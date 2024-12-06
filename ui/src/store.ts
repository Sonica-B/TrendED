import { computed } from 'vue';

const cache = {
  registrations: null,
};
export const registrations = computed({
  get() {
    if (cache.registrations === null) {
      const stored = localStorage.getItem('registrations');
      cache.registrations = stored !== null ? JSON.parse(stored) : [];
    }
    return cache.registrations;
  },
  set(registrations) {
    cache.registrations = registrations;
    localStorage.setItem('registrations', JSON.stringify(registrations));
  },
});
