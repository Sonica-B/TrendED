<script setup lang="ts">
import { ref, nextTick } from 'vue';
import { user } from '../store.ts';
import { Message, Dialog, Button, InputText } from 'primevue';
import { Form, type FormResolverOptions, type FormSubmitEvent } from '@primevue/forms';
import {
  parseCreationOptionsFromJSON,
  create as webauthnCreate,
  get as webauthnGet,
  supported as webauthnSupported,
  parseRequestOptionsFromJSON,
} from '@github/webauthn-json/browser-ponyfill';

const registerErrorMessage = ref('');
const authenticateErrorMessage = ref('');
const open = ref(false);
const newAccount = ref(false);

function registerResolver({ values }: FormResolverOptions) {
  console.log(values);
  const errors: Record<string, { message: string }[]> = {};
  if ((values.name?.length ?? 0) < 4) {
    errors.name = [{ message: 'Name must be at least 4 characters long' }];
  }
  if ((values.username?.length ?? 0) < 4) {
    errors.username = [{ message: 'Username must be at least 4 characters long' }];
  }
  return { errors };
}

const signInFocus = ref();
const registerFocus = ref();
const registerIntial = ref({});

function openRegister() {
  open.value = true;
  newAccount.value = false;
  nextTick(() => {
    signInFocus.value.$el.focus();
  });
}

async function register({ valid, states }: FormSubmitEvent) {
  if (!valid) return;
  const response = await fetch('http://localhost:8000/register', {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      name: states.name.value,
      username: states.username.value,
    }),
  });
  const json = await response.json();
  if (!response.ok) {
    registerErrorMessage.value = json.error;
    return;
  }
  const id: string = json.id;
  const cco = parseCreationOptionsFromJSON({
    publicKey: json.options,
  });
  console.log('cco', cco);

  delete cco.publicKey?.attestation;
  delete cco.publicKey?.rp.id;

  const webauthResp = await webauthnCreate(cco);

  console.log('webauthCreateResp', webauthResp);
  const verifyResp = await fetch('http://localhost:8000/register/verify', {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      resp: webauthResp.toJSON(),
      id,
    }),
  });

  const verifyJson = await verifyResp.json();
  if (!verifyResp.ok) {
    registerErrorMessage.value = verifyJson.error;
    return;
  }
  user.value = verifyJson.user;
  console.log('Verify Json Reg', verifyJson);
  document.cookie = `session=${verifyJson.session}`;
  open.value = false;
}

async function authenticate({ states }: FormSubmitEvent) {
  const response = await fetch('http://localhost:8000/authenticate', {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      username: states.username.value,
    }),
  });
  const json = await response.json();
  if (!response.ok) {
    authenticateErrorMessage.value = json.error;
    return;
  }
  const id: string = json.id;
  const gco = parseRequestOptionsFromJSON({
    publicKey: json.options,
  });
  console.log('gco', gco);

  const webauthResp = await webauthnGet(gco);

  console.log('webauthGetResp', webauthResp);

  const verifyResp = await fetch('http://localhost:8000/authenticate/verify', {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({
      resp: webauthResp.toJSON(),
      id,
    }),
  });

  const verifyJson = await verifyResp.json();
  if (!verifyResp.ok) {
    authenticateErrorMessage.value = verifyJson.error;
    return;
  }
  user.value = verifyJson.user;
  console.log('Verify Json', verifyJson);
  document.cookie = `session=${verifyJson.session}`;
  open.value = false;
}

async function logout() {
  await fetch('http://localhost:8000/logout', {
    method: 'POST',
    credentials: 'include',
  });
  user.value = null;
  document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  // invalidate session
}
</script>
<template>
  <Dialog
    v-model:visible="open"
    modal
    header="Register"
    position="topright"
    class="bg-opacity-50 p-4 backdrop-blur-2xl"
    :close-on-escape="true"
    :dismissable-mask="true"
  >
    <template #container="{}">
      <div v-if="webauthnSupported()" class="grid grid-rows-1 transition-[grid-template-rows]">
        <Form v-if="!newAccount" v-slot="$form" @submit="authenticate">
          <div class="flex flex-col gap-2">
            <div class="flex gap-2">
              <InputText
                ref="signInFocus"
                name="username"
                class="flex-auto"
                placeholder="jsmith"
                autocomplete="off"
              />
            </div>
            <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">
              {{ $form.username.error?.message }}
            </Message>
            <Message
              v-if="authenticateErrorMessage.length > 0"
              severity="error"
              size="small"
              variant="simple"
            >
              {{ authenticateErrorMessage }}
            </Message>
            <div class="flex gap-2">
              <Button
                variant="text"
                label="Create Account"
                @click="
                  () => {
                    registerIntial = { username: $form.username.value };
                    newAccount = true;
                    nextTick(() => registerFocus.$el.focus());
                  }
                "
              />
              <Button type="submit" label="Sign In" />
            </div>
          </div>
        </Form>
        <Form
          v-else
          v-slot="$form"
          :resolver="registerResolver"
          :initial-values="registerIntial"
          :validate-on-value-update="false"
          @submit="register"
        >
          <div class="mb-4 flex flex-col gap-2">
            <InputText
              ref="registerFocus"
              name="username"
              class="flex-auto"
              placeholder="jsmith"
              autocomplete="off"
            />
            <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">
              {{ $form.username.error?.message }}
            </Message>
            <InputText name="name" class="flex-auto" placeholder="John Smith" autocomplete="off" />
            <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
              {{ $form.name.error?.message }}
            </Message>
          </div>
          <Message
            v-if="registerErrorMessage.length > 0"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ registerErrorMessage }}
          </Message>
          <Button type="submit" variant="text" label="Create Account" />
        </Form>
      </div>
      <Message v-else severity="error" size="small" variant="simple">
        WebAuthn is not supported in this browser
      </Message>
    </template>
  </Dialog>
  <Button v-if="user === null" label="Login" @click="openRegister" />
  <Button v-else label="Logout" @click="logout" />
</template>
