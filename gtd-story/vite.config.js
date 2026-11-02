import { defineConfig } from 'vite';
export default defineConfig({
  base: '/',
  esbuild: { jsx: 'automatic' },
  build: {
    rollupOptions: {
      onwarn(warning, warn) {
        if (warning.code === 'MODULE_LEVEL_DIRECTIVE' && warning.message.includes('use client'))
          return;
        warn(warning);
      },
      output: {
        manualChunks(id) {
          if (id.includes('/three/')) return 'globe-engine';
          if (id.includes('/framer-motion/') || id.includes('/motion-')) return 'motion';
          if (id.includes('/react/') || id.includes('/react-dom/') || id.includes('/scheduler/'))
            return 'react';
        },
      },
    },
  },
});
