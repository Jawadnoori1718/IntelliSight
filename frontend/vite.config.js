import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// During development, requests to /api and /ws are proxied to the FastAPI
// backend (http://127.0.0.1:8000). This is used from Phase 4 onwards.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/ws': { target: 'ws://127.0.0.1:8000', ws: true },
    },
  },
})
