<script setup lang="ts">
import { computed, ref, nextTick } from 'vue';
import { registrations } from '../store.ts';
import { Message, Dialog, Button, InputText } from 'primevue';
import { Form, type FormResolverOptions, type FormSubmitEvent } from '@primevue/forms';
import type { PublicKeyCredentialDescriptorJSON } from '@github/webauthn-json';
import {
  parseCreationOptionsFromJSON,
  create as webauthnCreate,
  get as webauthnGet,
  supported as webauthnSupported,
  parseRequestOptionsFromJSON,
  type AuthenticationPublicKeyCredential,
} from '@github/webauthn-json/browser-ponyfill';

enum RegistrationState {
  None,
  Inputting,
  Waiting,
  Success,
  Error,
}

const registering = ref(RegistrationState.None);
const showRegisterDialog = computed(() =>
  [RegistrationState.Inputting, RegistrationState.Error].includes(registering.value)
);
function resolver({ values }: FormResolverOptions) {
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
const firstInput = ref();

function registeredCredentials(): PublicKeyCredentialDescriptorJSON[] {
  return (
    registrations.value?.map((reg) => ({
      id: reg.rawId,
      type: reg.type,
    })) ?? []
  );
}

function openRegister() {
  registering.value = RegistrationState.Inputting;
  nextTick(() => {
    firstInput.value.$el.focus();
  });
}

async function onRegisterSubmit({ valid, states }: FormSubmitEvent) {
  if (!valid) return;

  registering.value = RegistrationState.Waiting;
  try {
    await register(states.name.value, states.username.value);
    registering.value = RegistrationState.Success;
  } catch {
    registering.value = RegistrationState.Error;
  }
}

async function register(name: string, username: string): Promise<void> {
  // get id by contacting database
  // const id = await fetch('', {
  //   method: 'POST',
  //   headers: {
  //     'Content-Type': 'application/json',
  //   },
  //   body: JSON.stringify({
  //     name,
  //     username,
  //   }),
  // });
  const cco = parseCreationOptionsFromJSON({
    publicKey: {
      challenge: 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
      rp: { name: 'Localhost, Inc.' },
      user: {
        id: 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII',
        name: username,
        displayName: name,
      },
      pubKeyCredParams: [],
      excludeCredentials: registeredCredentials(),
      authenticatorSelection: { userVerification: 'discouraged' },
      extensions: {
        credProps: true,
      },
    },
  });
  try {
    registrations.value = [...(registrations.value ?? []), (await webauthnCreate(cco)).toJSON()];
  } catch {
    throw new Error('Failed to create credential');
  }
}

async function authenticate(): Promise<AuthenticationPublicKeyCredential> {
  const cro = parseRequestOptionsFromJSON({
    publicKey: {
      challenge: 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
      allowCredentials: registeredCredentials(),
      userVerification: 'discouraged',
    },
  });
  return webauthnGet(cro);
}
</script>
<template>
  <Dialog
    v-model:visible="showRegisterDialog"
    modal
    header="Register"
    position="topright"
    class="bg-opacity-50 p-4 backdrop-blur-2xl"
  >
    <template #container="{}">
      <Form
        v-slot="$form"
        :resolver
        :validate-on-value-update="false"
        @keydown.esc="registering = RegistrationState.None"
        @submit="onRegisterSubmit"
      >
        <div class="mb-4 flex flex-col gap-2">
          <InputText
            ref="firstInput"
            name="name"
            class="flex-auto"
            placeholder="John Smith"
            autocomplete="off"
          />
          <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
            {{ $form.name.error?.message }}
          </Message>
          <InputText name="username" class="flex-auto" placeholder="jsmith" autocomplete="off" />
          <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">
            {{ $form.username.error?.message }}
          </Message>
        </div>
        <div class="flex justify-end gap-2">
          <Button
            type="button"
            label="Cancel"
            severity="secondary"
            @click="registering = RegistrationState.None"
          />
          <Button type="submit" label="Register" />
        </div>
      </Form>
    </template>
  </Dialog>
  <div v-if="webauthnSupported()" class="flex items-center gap-2">
    <Button label="Sign In" @click="authenticate" />
    <Button label="Register" @click="openRegister" />
  </div>
  <Message v-else severity="warn" size="small">Passkeys Not Supported</Message>
</template>
