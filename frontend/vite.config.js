import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    tailwindcss(),
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      // forward /scan_document → Flask scanner
      '/scan_document': {
        target: 'http://localhost:9697',
        changeOrigin: true,
      },
      // forward /api (eg. /api/ai/analyse) → Flask AI‐wrapper
      '/api': {
        target: 'http://localhost:9697',
        changeOrigin: true,
      },
    }
  }
})
