<script setup lang="ts">
import LoginButton from '@/components/LoginButton.vue';
import { Job } from '@/lib/types';
import { user } from '@lib/auth';
import { computedAsync } from '@vueuse/core';
import { Button, Card, ProgressSpinner } from 'primevue';
import { Ref } from 'vue';

const jobs: Ref<Job[] | null> = computedAsync(async () => {
  if (user.value === null) return;

  const res = await fetch(
    `${import.meta.env.VITE_SERVER_ADDR}/jobs/find_jobs?${new URLSearchParams({
      courses: user.value.courseIds.join(','),
      top_n: (5).toString(),
    }).toString()}`
  );

  if (!res.ok) return null;

  const json = await res.json();
  if (json.error) return null;

  return json;
}, null);
</script>
<template>
  <section
    v-if="user === null"
    class="flex h-full w-full flex-col items-center justify-center gap-4 p-10 pb-0 text-center"
  >
    <h1 class="text-4xl font-semibold">TrendED Job Recommender</h1>
    <p class="text-xl">Get personalized job recommendations based on your courses and skills.</p>
    <div>
      <LoginButton position="center" default-mode="register">
        <template #signin="{ open }">
          <Button class="px-8 text-3xl" variant="outlined" label="Sign Up Now!" @click="open" />
        </template>
      </LoginButton>
    </div>
  </section>
  <section v-else class="flex flex-col items-center justify-center gap-8 p-8">
    <h1 class="text-center text-4xl font-semibold">Welcome back, {{ user.name }}</h1>
    <h2 class="text-center text-2xl text-surface-700 dark:text-surface-200">
      Here are some jobs you might be interested in
    </h2>
    <div class="flex w-full max-w-6xl flex-col gap-8">
      <div v-if="jobs === null" class="flex w-full justify-center">
        <ProgressSpinner stroke-width="4" />
      </div>
      <Card v-for="(job, i) in jobs" :key="i">
        <template #title>
          <a :href="job.url" class="hover:text-primary hover:underline">
            {{ job.title }}
          </a>
        </template>
        <template #subtitle>{{ job.employer }} | {{ job.location }}</template>
        <template #content> {{ job.description }}</template>
      </Card>
    </div>
  </section>
</template>
