import { createApp } from 'vue'
import '@/style.css'
import App from '@/App.vue'
import router from '@/router/index.js'
import store from './store/index.js'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/antd.css';
// import 'ant-design-vue/dist/antd.less'
import 'ant-design-vue/dist/antd.less'
// import 'ant-design-vue/dist/antd.less'

let app = createApp(App);

// 使用的组件
app.use(router);
app.use(store);
app.use(Antd);
app.mount('#app');

