/*
 * @Description: 配置文件
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-07-26 14:04:04
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2024-01-15 17:26:55
 */
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import legacy from '@vitejs/plugin-legacy'
import vueJsx from '@vitejs/plugin-vue-jsx'
import viteCompression from 'vite-plugin-compression'

import electron from "vite-plugin-electron"
import electronRenderer from "vite-plugin-electron-renderer"
import polyfillExports from "vite-plugin-electron-renderer"

const path = require('path')

function _resolve(dir: string) {
  return path.resolve(__dirname, dir);
}

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  return {
    plugins: [
      vue(),
      vueJsx(),
      legacy({
        targets: ['defaults', 'not IE 11'],
        additionalLegacyPolyfills: ['regenerator-runtime/runtime']
      }),
      viteCompression(),
      polyfillExports(),
    ],
    base: mode === 'development' ? '' : `/${loadEnv(mode, process.cwd()).VITE_APP_NAME}/`,
    build: {
      emptyOutDir: false, // 默认情况下，若 outDir 在 root 目录下，则 Vite 会在构建时清空该目录
      outDir: `${loadEnv(mode, process.cwd()).VITE_APP_NAME}`,
      target: "esnext",
      chunkSizeWarningLimit: 1500,
      sourcemap: false,
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      },
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules')) {
              return id
                .toString()
                .split('node_modules/')[1]
                .split('/')[0]
                .toString();
            }
          },
          chunkFileNames: (chunkInfo) => {
            const facadeModuleId = chunkInfo.facadeModuleId
              ? chunkInfo.facadeModuleId.split('/')
              : [];
            const fileName =
              facadeModuleId[facadeModuleId.length - 2] || '[name]';
            return `js/${fileName}/[name].[hash].js`;
          }
        }
      }
    },
    resolve: {
      alias: {
        '@': _resolve('src'),
        '#': _resolve('types')
      }
    },
    define: {
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'true'
    },
    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
        }
      },
    },
    server: {
      port: 8888,
      host: '0.0.0.0',
      proxy: {
        "/localApi": {
          target: `http://127.0.0.1:8891`,
          rewrite: path => path.replace(/^\/localApi/, ''),
          changeOrigin: true
        },
      }
    }
  }
})
