import { computed } from 'vue';
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
