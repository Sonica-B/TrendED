import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import App from './App.vue';
import 'primeicons/primeicons.css';
import './assets/tailwind.css';
import './style.css';
import { router } from '@lib/router.ts';

createApp(App)
  .use(router)
  .use(PrimeVue, {
    theme: 'none',
  })
  .mount('#app');
