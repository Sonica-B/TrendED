<script setup lang="ts">
import { ref, nextTick, type Ref } from 'vue';
import { Menu, Message, Dialog, Button, InputText, ProgressBar } from 'primevue';
import { Form, type FormResolverOptions, type FormSubmitEvent } from '@primevue/forms';
import { user, logout, login, register } from '@/lib/auth';
import { supported as webauthnSupported } from '@github/webauthn-json';

const registerErrorMessage = ref('');
const authenticateErrorMessage = ref('');
const open = ref(false);
const newAccount = ref(false);

const accountMenu = ref();

function openLoginPrompt() {
  open.value = true;
  newAccount.value = false;
  registerErrorMessage.value = '';
  authenticateErrorMessage.value = '';
  nextTick(() => {
    signInFocus.value.$el.focus();
  });
}

function closePrompt() {
  open.value = false;
}

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

async function updateWithAnim(ref: Ref<string>, str: string) {
  ref.value = '';
  await nextTick();
  ref.value = str;
}

const signInFocus = ref();
const registerFocus = ref();
const registerIntial = ref({});

const registerLoading = ref(false);
async function registration({ valid, states }: FormSubmitEvent) {
  if (!valid) return;
  registerLoading.value = true;
  try {
    await register(states.username.value ?? '', states.name.value ?? '');
    closePrompt();
  } catch (e) {
    if (e instanceof Error) updateWithAnim(registerErrorMessage, e.message);
  } finally {
    registerLoading.value = false;
  }
}

const authLoading = ref(false);
async function authenticate({ valid, states }: FormSubmitEvent) {
  if (!valid) return;
  authLoading.value = true;
  try {
    await login(states.username.value ?? '');
    closePrompt();
  } catch (e) {
    if (e instanceof Error) updateWithAnim(authenticateErrorMessage, e.message);
  } finally {
    authLoading.value = false;
  }
}
</script>
<template>
  <Dialog
    v-model:visible="open"
    modal
    header="Register"
    position="topright"
    class="overflow-clip bg-opacity-50 p-4 backdrop-blur-2xl"
    :close-on-escape="true"
    :dismissable-mask="true"
  >
    <template #container="{}">
      <div v-if="webauthnSupported()" class="grid grid-rows-1 transition-[grid-template-rows]">
        <Form v-if="!newAccount" v-slot="$form" @submit="authenticate">
          <div class="flex flex-col gap-2">
            <InputText
              ref="signInFocus"
              name="username"
              class="flex-auto"
              placeholder="jsmith"
              autocomplete="off"
            />
            <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">
              {{ $form.username.error?.message }}
            </Message>
            <Message
              v-if="authenticateErrorMessage.length > 0"
              severity="error"
              size="small"
              variant="simple"
              class="animate-shake"
            >
              {{ authenticateErrorMessage }}
            </Message>
            <div class="flex gap-2">
              <Button
                variant="text"
                label="Create Account"
                :disabled="authLoading"
                @click="
                  () => {
                    registerIntial = { username: $form.username.value };
                    newAccount = true;
                    nextTick(() => registerFocus.$el.focus());
                  }
                "
              />
              <Button type="submit" label="Sign In" :disabled="authLoading" />
            </div>
          </div>
          <ProgressBar
            mode="indeterminate"
            class="-mx-4 -mb-4 mt-3 h-1 duration-200"
            :class="{ 'opacity-0': !authLoading }"
          />
        </Form>
        <Form
          v-else
          v-slot="$form"
          :resolver="registerResolver"
          :initial-values="registerIntial"
          :validate-on-value-update="false"
          @submit="registration"
        >
          <div class="flex flex-col gap-2">
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
            <Message
              v-if="registerErrorMessage.length > 0"
              severity="error"
              size="small"
              variant="simple"
              class="animate-shake"
            >
              {{ registerErrorMessage }}
            </Message>
            <div class="flex gap-2">
              <Button
                variant="text"
                label="Back"
                :disabled="registerLoading"
                @click="openLoginPrompt"
              />
              <span class="flex-grow" />
              <Button type="submit" label="Create Account" :disabled="registerLoading" />
            </div>
          </div>
          <ProgressBar
            mode="indeterminate"
            class="-mx-4 -mb-4 mt-3 h-1 duration-200"
            :class="{ 'opacity-0': !registerLoading }"
          />
        </Form>
      </div>
      <Message v-else severity="error" size="small" variant="simple">
        WebAuthn is not supported in this browser
      </Message>
    </template>
  </Dialog>
  <Button v-if="user === null" label="Login" @click="openLoginPrompt" />
  <template v-else>
    <Button
      variant="text"
      class="flex gap-4 !text-color"
      severity="secondary"
      aria-haspopup="true"
      @click="accountMenu?.toggle"
    >
      {{ user.name }}
      <span class="pi pi-user" />
    </Button>
    <Menu
      ref="accountMenu"
      :model="[
        {
          label: 'Logout',
          icon: 'pi pi-sign-out',
          command: logout,
        },
      ]"
      :popup="true"
    />
  </template>
</template>
