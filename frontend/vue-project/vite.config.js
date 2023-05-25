import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0',
    port: 8765,
    // proxy: {
    //   '/recipes/v1': {
    //     target: 'http://backend:8765',
    //     changeOrigin: true,
    //     rewrite: (path) => path.replace(/^\/recipes\/v1/, '')
    //   }
    // }
  }
})
