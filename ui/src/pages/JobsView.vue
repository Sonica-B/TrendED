<script setup lang="ts">
import { jobs } from '@/lib/store';
import { Card } from 'primevue';
</script>
<template>
  <section class="flex flex-col gap-8 overflow-y-scroll p-8">
    <Card v-for="(job, i) in jobs" :key="i">
      <template #title>{{ job.title }}</template>
    </Card>
  </section>
</template>
