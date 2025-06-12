import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  preview: {
    host: true,
    port: 5173,
    strictPort: true,
    headers: {},
  },
  build: {
    target: 'esnext',
    minify: true
  }
});