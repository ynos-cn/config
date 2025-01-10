/*
 * @Description: 类型定义
 * @Version: 1.0
 * @Autor: jiajun wu
 * @Date: 2022-04-12 14:42:26
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2022-07-28 14:44:01
 */
/// <reference types="vite/client" />

import 'vue-router';
import { MessageApi } from 'ant-design-vue/lib/message'
import { Store } from 'vuex'
import { WebStorage } from 'ynos-storage/dist/src/WebStorage'
import { JsEvents } from '@/utils/Event'
import { RouterMeta } from '@/router/types'

declare module "@vue/runtime-core" {
  interface ComponentCustomProperties {
    $message: MessageApi
    ls: WebStorage
    $Events: JsEvents
  }
}

declare module 'vue-router' {
  interface RouteMeta extends RouterMeta {
  }
}
