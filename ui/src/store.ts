import { computed, Ref, ref } from 'vue';
import type { PublicKeyCredentialWithAttestationJSON } from '@github/webauthn-json';

const cache: {
  registrations?: PublicKeyCredentialWithAttestationJSON[];
} = {
  registrations: undefined,
};
export const registrations = computed({
  get() {
    if (cache.registrations === null) {
      const stored = localStorage.getItem('registrations');
      cache.registrations = stored !== null ? JSON.parse(stored) : [];
    }
    return cache.registrations;
  },
  set(registrations: PublicKeyCredentialWithAttestationJSON[]) {
    cache.registrations = registrations;
    localStorage.setItem('registrations', JSON.stringify(registrations));
  },
});

export type User = {
  id: string;
  name: string;
  username: string;
};
fetch('http://localhost:8000/api/user', {
  credentials: 'include',
})
  .then((response) => response.json())
  .then((data) => {
    user.value = data;
  })
  .catch(() => {});
export const user: Ref<User | null> = ref(null);
