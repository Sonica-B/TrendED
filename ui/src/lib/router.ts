import { createWebHistory, createRouter, type RouteRecordRaw } from 'vue-router';
import 'vue-router';

declare module 'vue-router' {
  interface RouteMeta {
    icon?: string;
  }
}

import Profile from '@pages/ProfileView.vue';
import Home from '@pages/HomeView.vue';
import Jobs from '@pages/JobsView.vue';

export const routes: RouteRecordRaw[] = [
  { path: '/', component: Home, name: 'Home', meta: { icon: 'home' } },
  { path: '/profile', component: Profile, name: 'Profile', meta: { icon: 'user' } },
  { path: '/jobs', component: Jobs, name: 'Jobs', meta: { icon: 'briefcase' } },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
