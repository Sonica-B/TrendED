<script setup lang="ts">
import { computed, ref, useTemplateRef, nextTick } from 'vue';
import { registrations } from './store.ts';
import HelloWorld from './components/HelloWorld.vue';
import { Message, Dialog, Menubar, Button, InputText, Card } from 'primevue';
import { Form } from '@primevue/forms';
import { type PublicKeyCredentialDescriptorJSON } from '@github/webauthn-json';
import {
  parseCreationOptionsFromJSON,
  create,
  get,
  parseRequestOptionsFromJSON,
  supported,
  AuthenticationPublicKeyCredential,
} from '@github/webauthn-json/browser-ponyfill';

enum RegistrationState {
  None,
  Inputting,
  Waiting,
  Success,
  Error,
}

const text = ref('');
const msg = ref('');

function greet() {
  msg.value = 'Hello ' + text.value;
}

const registering = ref(RegistrationState.None);
const showRegisterDialog = computed(() =>
  [RegistrationState.Inputting, RegistrationState.Error].includes(registering.value)
);
const registrationForm = ref();
function resolver({ values }) {
  console.log(values);
  const errors = {};
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
  return registrations.value.map((reg) => ({
    id: reg.rawId,
    type: reg.type,
  }));
}

function openRegister() {
  registering.value = RegistrationState.Inputting;
  nextTick(() => {
    firstInput.value.$el.focus();
  });
}

async function onRegisterSubmit({ valid, states }) {
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
    await create(cco);
  } catch {}
}

async function authenticate(options?: {
  conditionalMediation?: boolean;
}): Promise<AuthenticationPublicKeyCredential> {
  const cro = parseRequestOptionsFromJSON({
    publicKey: {
      challenge: 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC',
      allowCredentials: registeredCredentials(),
      userVerification: 'discouraged',
    },
  });
  return get(cro);
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
        :resolver
        v-slot="$form"
        @keydown.esc="registering = RegistrationState.None"
        @submit="onRegisterSubmit"
        :validateOnValueUpdate="false"
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
  <nav class="fixed left-0 top-0 w-full">
    <Menubar class="rounded-none border-0 border-b bg-transparent backdrop-blur">
      <template #start>
        <span class="text-2xl font-semibold"> TrendED </span>
      </template>
      <template #end>
        <div class="flex items-center gap-2">
          <InputText placeholder="Search" type="text" class="w-32 sm:w-auto" />
          <Button label="Sign In" @click="authenticate" />
          <Button label="Register" @click="openRegister" />
        </div>
      </template>
    </Menubar>
  </nav>
  <section class="flex max-w-3xl flex-col gap-8 rounded-xl bg-white p-10 pt-20 dark:bg-surface-900">
    <h1 class="text-center text-4xl font-bold text-black dark:text-white">
      Tailwind CSS + PrimeVue
    </h1>
    <Card class="bg-surface-200 dark:bg-surface-800">
      <template #title> Buttons </template>
      <template #content>
        <div class="flex flex-col flex-wrap justify-center gap-2 sm:flex-row">
          <HelloWorld
            v-for="(m, i) in ['Message one', 'Another message', '3']"
            :key="i"
            class="flex-grow sm:flex-grow-0"
            :msg="m"
          />
        </div>
      </template>
    </Card>
    <form class="flex gap-4" @submit.prevent="greet">
      <InputText v-model="text" maxlength="20" fluid />
      <Button label="Submit" class="min-w-20" :disabled="text.length === 0" type="submit" />
    </form>
    <div
      class="grid grid-rows-[0fr] text-center text-xl text-primary transition-[grid-template-rows]"
      :class="{
        'grid-rows-[1fr]': msg.length > 0,
      }"
    >
      <div class="overflow-hidden">
        {{ msg }}
      </div>
    </div>
  </section>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
