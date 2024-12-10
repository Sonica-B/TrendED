<script setup lang="ts">
import { Form } from '@primevue/forms';
import { Course } from '@lib/types.ts';
import { AutoComplete, Card, Textarea } from 'primevue';
import { ref, type Ref } from 'vue';

const courses: Ref<Course[]> = ref([]);
</script>
<template>
  <section class="m-4 flex flex-col gap-8 rounded-xl bg-white p-4 dark:bg-surface-900">
    <Form class="flex flex-col text-black dark:text-white">
      <label for="desc"></label>
      <Textarea id="desc" />
      <AutoComplete :suggestions=""/>
      <Card v-for="course in courses" :key="course.code" class="bg-surface-200 dark:bg-surface-800">
        <template #title>
          <span> COde: {{ course.code }}</span>
        </template>
        <template #content>
          <span>{{ JSON.stringify(course) }}</span>
        </template>
      </Card>
    </Form>
  </section>
</template>
