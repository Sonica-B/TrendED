<script setup lang="ts">
import { Menubar } from 'primevue';
import LoginButton from './components/LoginButton.vue';
import { router } from '@lib/router';
import { MenuItem } from 'primevue/menuitem';
import { user } from './lib/auth';

const routes: MenuItem[] = router
  .getRoutes()
  .map((v) => ({
    url: v.path,
    label: v.name?.toString(),
    icon: v.meta.icon,
    auth: v.meta.auth,
  }))
  .filter((v) => v !== null);
</script>

<template>
  <Menubar
    class="fixed left-0 top-0 w-full rounded-none border-0 border-b bg-transparent backdrop-blur"
    breakpoint="600px"
    :model="routes"
  >
    <template #start>
      <span class="text-2xl font-semibold"> TrendED </span>
    </template>
    <template #item="{ item, props }">
      <RouterLink
        v-if="item.url && !(item.auth && user === null)"
        v-slot="{ href, navigate, isExactActive }"
        :to="item.url"
        custom
      >
        <a
          :href="href"
          v-bind="props.action"
          :class="{
            'text-primary': isExactActive,
          }"
          @click="navigate"
        >
          <span v-if="item.icon" :class="`pi pi-${item.icon}`" />
          <span>{{ item.label }}</span>
        </a>
      </RouterLink>
    </template>
    <template #end>
      <LoginButton />
    </template>
  </Menubar>
  <main class="h-full pt-14">
    <RouterView />
  </main>
</template>
