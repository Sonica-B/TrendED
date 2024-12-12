import { createWebHistory, createRouter, type RouteRecordRaw } from 'vue-router';
import 'vue-router';
import { isAuth } from '@lib/auth';

declare module 'vue-router' {
  interface RouteMeta {
    icon?: string;
    auth: boolean;
  }
}

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@pages/HomeView.vue'),
    name: 'Home',
    meta: { icon: 'home', auth: false },
  },
  {
    path: '/jobs',
    component: () => import('@pages/JobsView.vue'),
    name: 'Jobs',
    meta: { icon: 'briefcase', auth: true },
  },
  {
    path: '/profile',
    component: () => import('@pages/ProfileView.vue'),
    name: 'Profile',
    meta: { icon: 'user', auth: true },
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
router.beforeEach(async (to) => {
  if (to.meta.auth && !(await isAuth())) return { path: '/' };
});
