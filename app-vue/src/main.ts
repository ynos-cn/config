/*
 * @Description: 应用入口
 * @Version: 1.0
 * @Autor: jiajun wu
 * @Date: 2021-11-11 11:56:17
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2024-01-15 16:42:33
 */
import { createApp } from 'vue'
import 'ant-design-vue/dist/reset.css';
import Antd, { message } from 'ant-design-vue'
import router from './router'
import { createPinia } from 'pinia'

import './permission'

import dayjs from 'dayjs'
import { onCacheCleanup } from '@/utils/utils';
import { EventBus } from '@/utils/Event'
import { LocalStorage } from '@/utils/storage'
import App from './App.vue'
import weekOfYear from 'dayjs/plugin/weekOfYear'
import isoWeek from 'dayjs/plugin/weekOfYear'
import BaseTable from './components/base-table/index'
import ZSelect from '@/components/z-select'

dayjs.extend(weekOfYear)
dayjs.extend(isoWeek)
dayjs.locale('zh-cn');

const app = createApp(App);
const pinia = createPinia()

onCacheCleanup(() => {
  LocalStorage.clear()
})

app.config.globalProperties.$message = message;
app
  .component(BaseTable.name as string, BaseTable)
  .component(ZSelect.name as string, ZSelect)
  .use(pinia)
  .use(Antd)
  .use(router)
  .use(EventBus)
  .mount('#app')
