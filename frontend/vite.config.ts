import { defineConfig } from "vite";
import dyadComponentTagger from "@dyad-sh/react-vite-component-tagger";
import react from "@vitejs/plugin-react-swc";
import path from "path";

export default defineConfig(() => ({
  // Set base path for GitHub Pages deployment
  // Use '/' for other deployments (Vercel, Netlify, etc.)
  base: process.env.GITHUB_PAGES === 'true' ? '/FinSense/' : '/',
  server: {
    host: "::",
    port: 5137,
  },
  plugins: [dyadComponentTagger(), react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
}));
