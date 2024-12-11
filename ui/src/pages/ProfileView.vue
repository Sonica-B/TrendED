<script setup lang="ts">
import { updateUser, user } from '@/lib/auth';
import { Course } from '@lib/types.ts';
import { Button, AutoComplete, DataTable, Divider, Column } from 'primevue';
import { computed, ref, type Ref } from 'vue';
import { AutoCompleteCompleteEvent } from 'primevue/autocomplete';
import { Form, type FormSubmitEvent } from '@primevue/forms';
import { asyncComputed } from '@vueuse/core';

const allCourses: Ref<Course[] | null> = asyncComputed(async () => {
  const res = await fetch(
    `${import.meta.env.VITE_SERVER_ADDR}/courses/get_courses?${new URLSearchParams({
      department: 'All',
    }).toString()}`
  );
  if (!res.ok) return [];
  return await res.json();
}, null);

const filteredCourses: Ref<Course[]> = ref([]);
function search(event: AutoCompleteCompleteEvent) {
  const query = event.query.toLowerCase();
  filteredCourses.value =
    allCourses.value?.filter((v) => v.code.toLowerCase().includes(query)) ?? [];
}

const courseMap = computed(() => {
  const map = new Map<string, Course>();
  for (const course of allCourses.value ?? []) {
    map.set(course.code, course);
  }
  return map;
});

const saving = ref(false);
async function addSelected({ states }: FormSubmitEvent) {
  saving.value = true;
  try {
    const courses = new Set([
      ...(user.value?.courseIds ?? []),
      ...states.courses.value.map((v: Course) => v.code),
    ]);
    if (user.value !== null) {
      user.value.courseIds = Array.from(courses);
      await updateUser();
    }
  } finally {
    saving.value = false;
  }
}
</script>
<template>
  <section class="mx-auto max-w-4xl flex-col justify-center rounded-xl p-8">
    <div class="mb-4 text-3xl">Manage Your Courses</div>
    <Form v-slot="$form" class="flex flex-wrap gap-4" @submit="addSelected">
      <AutoComplete
        :suggestions="filteredCourses"
        :option-label="(v) => v.code"
        :delay="0"
        :auto-option-focus="true"
        dropdown
        dropdown-mode="current"
        name="courses"
        multiple
        class="flex-grow"
        placeholder="Courses"
        @complete="search"
      />
      <Button
        type="submit"
        :label="`Add Course${($form.courses?.value?.length ?? 0) > 1 ? 's' : ''}`"
        :disabled="saving"
        :loading="saving"
      />
    </Form>
    <Divider />
    <DataTable
      :value="(user?.courseIds ?? []).map((v) => courseMap.get(v)).filter((v) => v !== undefined)"
    >
      <Column field="department" header="Department" />
      <Column field="title" header="Title" />
      <Column field="code" header="Code" />
      <Column field="description" header="Description" />
    </DataTable>
  </section>
</template>
