<script setup lang="ts">
import { user } from '@lib/auth';
</script>
<template>
  <div class="flex h-full w-full justify-center align-middle">
    <section class="m-4 flex w-full max-w-4xl flex-col gap-8 p-10">
      <h1 class="text-center text-4xl font-bold">
        {{ user === null ? 'Tailwind CSS + PrimeVue' : `Welcome, ${user.name}` }}
        <br />
      </h1>
      <h2 class="text-2xl text-surface-200">Here are some jobs you might be interested in:</h2>
    </section>
  </div>
</template>
