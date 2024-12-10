import { createWebHistory, createRouter, type RouteRecordRaw } from 'vue-router';
import 'vue-router';

declare module 'vue-router' {
  interface RouteMeta {
    icon?: string;
  }
}

import Profile from '@pages/ProfileView.vue';
import HomeView from '@pages/HomeView.vue';

export const routes: RouteRecordRaw[] = [
  { path: '/', component: HomeView, name: 'Home', meta: { icon: 'home' } },
  { path: '/profile', component: Profile, name: 'Profile', meta: { icon: 'user' } },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
