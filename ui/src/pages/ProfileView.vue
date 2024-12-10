<script setup lang="ts">
import { user } from '@/lib/store';
import { Course } from '@lib/types.ts';
import { Button, AutoComplete, DataTable, Divider, Column } from 'primevue';
import { computed, ref, type Ref } from 'vue';
import { AutoCompleteCompleteEvent } from 'primevue/autocomplete';
import { Form, type FormSubmitEvent } from '@primevue/forms';

const allCourses: Ref<Course[]> = ref(
  [...new Array(100)].map((_, i) => ({
    code: `CS${500 + i}`,
    description: `Course ${500 + i}`,
  }))
);
const filteredCourses: Ref<Course[]> = ref([]);
function search(event: AutoCompleteCompleteEvent) {
  const query = event.query.toLowerCase();
  filteredCourses.value = allCourses.value.filter((v) => v.code.toLowerCase().includes(query));
}

const courseMap = computed(() =>
  allCourses.value.reduce((a, v) => {
    a.set(v.code, v);
    return a;
  }, new Map<string, Course>())
);

function addSelected({ states }: FormSubmitEvent) {
  const courses = new Set([
    ...(user.value?.coursesIds ?? []),
    ...states.courses.value.map((v: Course) => v.code),
  ]);
  if (user.value !== null) {
    user.value.coursesIds = Array.from(courses);
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
      />
    </Form>
    <Divider />
    <DataTable
      :value="(user?.coursesIds ?? []).map((v) => courseMap.get(v)).filter((v) => v !== undefined)"
    >
      <Column field="code" header="Code" />
      <Column field="description" header="Description" />
    </DataTable>
  </section>
</template>
