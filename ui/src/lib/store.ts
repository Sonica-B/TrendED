import { Ref, ref } from 'vue';
import { computedAsync } from '@vueuse/core';
import { Job, User } from './types';

export const user: Ref<User | null> = ref(null);

export const jobs: Ref<Job[] | null> = computedAsync(
  async () => {
    const res = await fetch(`${import.meta.env.VITE_SERVER_ADDR}/`);
    if (res.ok) {
      return await res.json();
    } else {
      return null;
    }
  },
  null,
  { lazy: true }
);
