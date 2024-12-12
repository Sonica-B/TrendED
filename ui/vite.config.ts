import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components/'),
      '@lib': path.resolve(__dirname, './src/lib/'),
      '@pages': path.resolve(__dirname, './src/pages/'),
    },
  },
  plugins: [vue()],
  base: '/static',
});
