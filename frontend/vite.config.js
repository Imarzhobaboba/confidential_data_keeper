import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  preview: {
    host: true,
    port: 4173,
    strictPort: true,
    headers: {
      "Content-Security-Policy": "script-src 'self' 'unsafe-inline'"
    }
  },
  build: {
    target: 'esnext',
    minify: true
  }
})