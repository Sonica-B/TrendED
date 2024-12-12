<script setup lang="ts">
import { user } from '@/lib/auth';
import { Job } from '@/lib/types';
import { watchImmediate } from '@vueuse/core';
import {
  Button,
  Card,
  Divider,
  FloatLabel,
  ProgressBar,
  ProgressSpinner,
  InputText,
  ToggleSwitch,
} from 'primevue';
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

const jobs: Ref<Job[] | 'loading' | 'no-jobs' | 'error'> = ref('loading');

async function updateJobs() {
  jobs.value = 'loading';
  const courses = [...selectedCourses.entries()]
    .filter(([, selected]) => selected)
    .map(([course]) => course);
  if (courses.length === 0) {
    jobs.value = 'no-jobs';
    return;
  }
  prevCourses.value = [...selectedCourses.entries()];
  const res = await fetch(
    `${import.meta.env.VITE_SERVER_ADDR}/jobs/find_jobs?${new URLSearchParams({
      courses: courses.join(','),
      top_n: (50).toString(),
    }).toString()}`
  );

  const json = await res.json();

  if (!res.ok) {
    jobs.value = 'error';
    return;
  }

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
const prevCourses: Ref<[string, boolean][]> = ref([]);
const updatePending = computed(
  () =>
    prevCourses.value.length !== selectedCourses.size ||
    !prevCourses.value.every(([course, selected]) => selectedCourses.get(course) === selected)
);
</script>
<template>
  <div class="justify-center gap-8 sm:flex sm:h-full sm:flex-row sm:overflow-y-hidden">
    <section class="flex flex-col p-4 sm:h-full sm:flex-shrink-0 sm:self-start sm:p-8 sm:pr-0">
      <Button
        label="Find Jobs"
        :disabled="jobs === 'loading'"
        :severity="updatePending ? 'primary' : 'secondary'"
        @click="updateJobs"
      />
      <ProgressBar
        :class="{
          '!opacity-0': jobs !== 'loading',
        }"
        mode="indeterminate"
        class="h-1 opacity-100 transition-opacity duration-200"
      />
      <Divider />
      <div class="space-y-4">
        <FloatLabel variant="on">
          <label for="filtercourses">Filter Courses</label>
          <InputText id="filtercourses" v-model="filter" type="search" />
        </FloatLabel>
        <div class="flex">
          <span class="font-bold">Toggle Shown</span>
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
      <div v-if="jobs === 'loading'" class="flex w-full justify-center">
        <ProgressSpinner stroke-width="4" />
      </div>
      <div v-else-if="jobs === 'no-jobs'" class="text-center">
        <p class="pb-2 text-2xl">No jobs found.</p>
        <p class="text-xl text-muted-color">Make sure to select at least one course</p>
      </div>
      <div v-else-if="jobs === 'error'" class="w-full text-center">
        <p class="text-xl">An unknown error occured when trying to load jobs.</p>
      </div>
      <Card v-for="(job, i) in jobs" v-else :key="i">
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
