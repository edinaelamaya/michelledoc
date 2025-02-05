import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    strictPort: true,
    port: 6800,
    watch: {
      usePolling: true,
      interval: 100
    },
    hmr: {
      host: 'localhost',
      port: 6800
    }
  },
  preview: {
    port: 6800,
    host: '0.0.0.0'
  },
  base: '/',
  resolve: {
    alias: {
      '@': '/src'
    }
  }
})
