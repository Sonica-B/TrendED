<script setup lang="ts">
import { user } from '@/lib/auth';
import { Job } from '@/lib/types';
import { computedAsync } from '@vueuse/core';
import { Card } from 'primevue';
import { type Ref } from 'vue';

const jobs: Ref<Job[] | null> = computedAsync(async () => {
  console.log('computed', user.value);
  if (user.value === null) {
    return;
  }
  const url = `${import.meta.env.VITE_SERVER_ADDR}/jobs/find_jobs?${new URLSearchParams({
    courses: user.value.courseIds.join(','),
  }).toString()}`;
  console.log(url);
  const res = await fetch(url);

  if (!res.ok) {
    console.log('fail');
    return null;
  }
  const json = await res.json();
  if (json.error) {
    console.log(json.error);
    return null;
  }
  return json;
}, null);
</script>
<template>
  <section class="flex flex-col gap-8 p-8">
    <Card v-for="(job, i) in jobs" :key="i">
      <template #title>{{ job.title }}</template>
      <template #content> {{ JSON.stringify(job, null, 2) }}</template>
    </Card>
  </section>
</template>
