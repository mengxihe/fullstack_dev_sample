import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import Components from 'unplugin-vue-components/vite'
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
    Components({
      resolvers: [AntDesignVueResolver()],
    }),
  ],
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server:{
    host:'0.0.0.0'
  },
  css:{
    preprocessorOptions: {
      less: {
        modifyVars: {
          'primary-color': '#000000',
          'link-color': '#000000',
          'border-radius-base': '2px',
        },
        javascriptEnabled: true,
      },
    },
  }
})
