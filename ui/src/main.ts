import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import App from './App.vue';
import 'primeicons/primeicons.css';
import './assets/tailwind.css';
import './style.css';
import { router } from '@lib/router.ts';
import { user } from './lib/store';

// Fetch the user data in the background
fetch(`${import.meta.env.VITE_SERVER_ADDR}/api/user`, {
  credentials: 'include',
})
  .then((response) => response.json())
  .then((data) => {
    user.value = data;
  })
  .catch(() => {});

createApp(App)
  .use(router)
  .use(PrimeVue, {
    theme: 'none',
  })
  .mount('#app');
