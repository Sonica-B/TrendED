<script setup lang="ts">
import { user } from '@/lib/auth';
import { Job } from '@/lib/types';
import { watchImmediate } from '@vueuse/core';
import { Button, Card, Divider, ProgressSpinner, InputText, ToggleSwitch } from 'primevue';
import { nextTick, reactive, ref, computed, type Ref, type Reactive } from 'vue';
import ufuzzy from '@leeoniya/ufuzzy';

const selectedCourses: Reactive<Map<string, boolean>> = reactive(new Map());
watchImmediate(user, () => {
  if (user.value === null) {
    selectedCourses.clear();
    return;
  }
  const newCourses = new Set(user.value.courseIds);
  for (const course of selectedCourses.keys()) {
    if (!newCourses.has(course)) {
      selectedCourses.delete(course);
    }
  }
  for (const course of newCourses) {
    if (!selectedCourses.has(course)) {
      selectedCourses.set(course, true);
    }
  }
  nextTick(updateJobs);
});

const jobs: Ref<Job[] | null> = ref(null);
const loading = ref(false);

async function updateJobs() {
  loading.value = true;
  const res = await fetch(
    `${import.meta.env.VITE_SERVER_ADDR}/jobs/find_jobs?${new URLSearchParams({
      courses: [...selectedCourses.entries()]
        .filter(([, selected]) => selected)
        .map(([course]) => course)
        .join(','),
      top_n: (50).toString(),
    }).toString()}`
  );
  loading.value = false;

  if (!res.ok) return null;

  const json = await res.json();
  if (json.error) return null;

  jobs.value = json;
}

function toggleAll(state: boolean) {
  for (const course of filteredCourses.value) {
    selectedCourses.set(course, state);
  }
}

const filter = ref('');
const courses_uf = new ufuzzy({});
const filteredCourses = computed(() => {
  const courses = [...selectedCourses.keys()];
  return courses_uf.search(courses, filter.value, 1)[0]?.map((i) => courses[i]) ?? courses;
});
</script>
<template>
  <div class="justify-center gap-8 sm:flex sm:h-full sm:flex-row sm:overflow-y-hidden">
    <section class="flex flex-col p-4 sm:h-full sm:flex-shrink-0 sm:self-start sm:p-8 sm:pr-0">
      <h2 class="text-2xl">Filter Courses</h2>
      <Button variant="text" label="Update" :loading @click="updateJobs" />
      <Divider />
      <div class="space-y-4">
        <InputText v-model="filter" placeholder="Filter" type="search" />
        <div class="flex">
          <span class="font-bold">Toggle All</span>
          <span class="flex-grow" />
          <ToggleSwitch :model-value="true" @value-change="toggleAll" />
        </div>
      </div>
      <Divider />
      <div class="px-2 sm:flex-grow sm:overflow-y-auto">
        <div class="grid grid-cols-[minmax(0,1fr),auto] items-center gap-4">
          <template v-for="course in filteredCourses" :key="course">
            <span>{{ course }}</span>
            <ToggleSwitch
              :model-value="selectedCourses.get(course) ?? false"
              @value-change="(v) => selectedCourses.set(course, v)"
            />
          </template>
        </div>
      </div>
    </section>
    <section
      class="flex h-full w-full max-w-6xl flex-col gap-8 p-4 sm:overflow-y-auto sm:p-8 sm:pl-0"
    >
      <div v-if="jobs === null" class="flex w-full justify-center">
        <ProgressSpinner stroke-width="4" />
      </div>
      <Card v-for="(job, i) in jobs" :key="i">
        <template #title>
          <a :href="job.url" class="underline hover:text-primary">
            {{ job.title }}
          </a>
        </template>
        <template #subtitle>{{ job.employer }} | {{ job.location }}</template>
        <template #content> {{ job.description }}</template>
      </Card>
    </section>
  </div>
</template>
