import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "node:path";

const workspaceRoot = resolve(__dirname, "..");

export default defineConfig({
  plugins: [react()],
  publicDir: resolve(workspaceRoot, "media"),
  server: {
    port: 5173,
    strictPort: false,
    fs: {
      allow: [workspaceRoot],
    },
  },
});
