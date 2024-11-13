import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import App from './App.vue';
import './assets/tailwind.css';
import './style.css';

createApp(App)
  .use(PrimeVue, {
    theme: 'none',
  })
  .mount('#app');
