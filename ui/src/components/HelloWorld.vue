<script setup lang="ts">
import { Button, Card } from 'primevue';
import { ref } from 'vue';

defineProps<{ msg: string }>();

const count = ref(0);
</script>
<template>
  <Card>
    <template #title>{{ msg }}</template>
    <template #content>
      <Button @click="count++">count is {{ count }}</Button>
    </template>
  </Card>
</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
