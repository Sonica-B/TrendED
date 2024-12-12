<script setup lang="ts">
import { updateUser, user } from '@/lib/auth';
import { Course } from '@lib/types.ts';
import {
  Button,
  AutoComplete,
  DataTable,
  Divider,
  Message,
  Column,
  FloatLabel,
  InputText,
  AutoCompleteCompleteEvent,
} from 'primevue';
import { computed, ref, type Ref } from 'vue';
import { Form, type FormSubmitEvent, type FormResolverOptions } from '@primevue/forms';
import { asyncComputed } from '@vueuse/core';
import ufuzzy from '@leeoniya/ufuzzy';

function infoResolver({ values }: FormResolverOptions) {
  const errors: Record<string, { message: string }[]> = {};
  if ((values.name?.length ?? 0) < 4) {
    errors.name = [{ message: 'Name must be at least 4 characters long' }];
  }
  return { errors };
}

async function saveInfo({ states, valid }: FormSubmitEvent) {
  if (user.value === null || !valid) return;
  saving.value = true;
  try {
    user.value.name = states.name.value;
    await updateUser();
  } finally {
    saving.value = false;
  }
}

// Skills
const skills_uf = new ufuzzy({
  intraIns: 1,
});
const allSkills: Ref<string[] | null> = asyncComputed(async () => {
  const res = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/courses/get_skills`);
  if (!res.ok) return [];
  return await res.json();
}, null);
const filteredSkills: Ref<string[]> = ref([]);

function filterSkills(event: AutoCompleteCompleteEvent) {
  if (allSkills.value === null) {
    filteredSkills.value = [];
    return;
  }
  const skills = allSkills.value;
  filteredSkills.value =
    skills_uf.search(skills, event.query, 1)[0]?.map((i) => skills[i]) ?? allSkills.value;
  filteredSkills.value?.push(event.query);
}

async function addSelectedSkills({ states, reset }: FormSubmitEvent) {
  if (user.value === null || !states.skills.value) return;
  saving.value = true;
  try {
    user.value.skills = Array.from(new Set([...user.value.skills, ...states.skills.value]));
    await updateUser();
    reset();
  } finally {
    saving.value = false;
  }
}

async function removeSkill(skill: string) {
  if (user.value === null) return;
  user.value.skills = user.value.skills.filter((v) => v !== skill);
  await updateUser();
}

// Courses
const courses_uf = new ufuzzy({});
const expandedRows = ref();
const courseMap = computed(() => {
  const map = new Map<string, Course>();
  for (const course of allCourses.value ?? []) {
    map.set(course.code, course);
  }
  return map;
});
const saving = ref(false);

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
function filterCourses(event: AutoCompleteCompleteEvent) {
  if (allCourses.value === null) {
    filteredCourses.value = [];
    return;
  }
  const courses = allCourses.value;
  filteredCourses.value =
    courses_uf
      .search(
        courses.map((v) => v.code),
        event.query,
        1
      )[0]
      ?.map((i) => courses[i]) ?? courses;
}

async function addSelectedCourses({ states, reset }: FormSubmitEvent) {
  if (user.value === null || !states.courses) return;
  saving.value = true;
  try {
    user.value.courseIds = Array.from(
      new Set([
        ...(user.value?.courseIds ?? []),
        ...states.courses.value.map((v: Course) => v.code),
      ])
    );
    await updateUser();
    reset();
  } finally {
    saving.value = false;
  }
}

async function removeCourse(course: Course) {
  if (user.value === null) return;
  user.value.courseIds = user.value.courseIds.filter((v) => v !== course.code);
  await updateUser();
}
</script>

<template>
  <section class="mx-auto max-w-4xl flex-col justify-center rounded-xl p-8">
    <div class="mb-4 text-3xl">Update Info</div>
    <Form
      v-slot="$form"
      :initial-values="{
        name: user?.name,
      }"
      :resolver="infoResolver"
      class="flex flex-col items-start gap-4"
      @submit="saveInfo"
    >
      <div>
        <FloatLabel variant="on">
          <label for="name">Name</label>
          <InputText id="name" name="name" />
        </FloatLabel>
        <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple">
          {{ $form.name.error?.message }}
        </Message>
      </div>
      <Button type="submit" label="Save" :disabled="saving" />
    </Form>
    <Divider />
    <div class="mb-4 text-3xl">Your Skills</div>
    <Form v-slot="$form" class="flex flex-wrap gap-4" @submit="addSelectedSkills">
      <AutoComplete
        :auto-option-focus="true"
        dropdown
        dropdown-mode="blank"
        name="skills"
        :delay="0"
        multiple
        class="flex-grow"
        placeholder="Skills"
        :suggestions="filteredSkills"
        :model-value="$form?.skills?.value ?? []"
        @complete="filterSkills"
      />
      <Button
        type="submit"
        :label="`Add Skill${($form.courses?.value?.length ?? 0) > 1 ? 's' : ''}`"
        :disabled="saving"
      />
    </Form>
    <div class="flex flex-wrap gap-2 p-4">
      <div v-if="user && user.skills.length === 0" class="text-xl">Add some skills!</div>
      <div
        v-for="(skill, i) in user?.skills ?? []"
        v-else
        :key="i"
        class="overflow-clip rounded-full border border-surface-200 bg-surface-0 py-1 pl-4 text-lg dark:border-surface-700 dark:bg-surface-900"
      >
        {{ skill }}
        <Button
          icon="pi pi-trash"
          variant="text"
          :rounded="true"
          severity="danger"
          class="-my-2"
          @click="removeSkill(skill)"
        />
      </div>
    </div>
    <Divider />
    <div class="mb-4 text-3xl">Your Courses</div>
    <Form v-slot="$form" class="flex flex-wrap gap-4" @submit="addSelectedCourses">
      <AutoComplete
        :suggestions="filteredCourses"
        :option-label="(v) => v.code"
        :delay="100"
        :auto-option-focus="true"
        :model-value="$form?.courses?.value ?? []"
        dropdown
        dropdown-mode="blank"
        name="courses"
        multiple
        class="flex-grow"
        placeholder="Courses"
        @complete="filterCourses"
      />
      <Button
        type="submit"
        :label="`Add Course${($form.courses?.value?.length ?? 0) > 1 ? 's' : ''}`"
        :disabled="saving"
      />
    </Form>
    <Divider />
    <DataTable
      v-model:expanded-rows="expandedRows"
      :value="(user?.courseIds ?? []).map((v) => courseMap.get(v)).filter((v) => v !== undefined)"
      removable-sort
      paginator
      :rows="10"
      :rows-per-page-options="[5, 10, 20, 100]"
      class="overflow-clip rounded-lg border dark:border-0"
    >
      <Column expander class="w-14" />
      <Column sortable field="department" header="Department" />
      <Column sortable field="title" header="Title" />
      <Column sortable field="code" header="Code" />
      <Column class="w-14">
        <template #body="{ data }">
          <Button icon="pi pi-trash" variant="text" severity="danger" @click="removeCourse(data)" />
        </template>
      </Column>
      <template #expansion="{ data }: { data: Course }">
        {{ data.description }}
      </template>
    </DataTable>
  </section>
</template>
