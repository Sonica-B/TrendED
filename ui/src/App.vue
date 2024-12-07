<script setup lang="ts">
import { ref } from 'vue';
import LoginCard from './components/LoginCard.vue';
import HelloWorld from './components/HelloWorld.vue';
import { Menubar, Button, InputText, Card } from 'primevue';

const text = ref('');
const msg = ref('');

function greet() {
  msg.value = 'Hello ' + text.value;
}
</script>

<template>
  <nav class="fixed left-0 top-0 w-full">
    <Menubar class="rounded-none border-0 border-b bg-transparent backdrop-blur">
      <template #start>
        <span class="text-2xl font-semibold"> TrendED </span>
      </template>
      <template #end>
        <LoginCard />
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
