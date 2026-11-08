import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // dev only: browser calls localhost:5173/api/... -> Vite forwards to the backend
      '/api': 'http://127.0.0.1:8000',
    },
  },
})