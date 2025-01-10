/*
 * @Description: 空白布局
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-07-27 11:21:34
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2022-07-28 14:21:09
 */

import { defineComponent, h } from 'vue'
import RouteView from './route-view'
import classses from './index.module.less'

const BlankLayout = defineComponent({
  name: 'BlankLayout',
  setup() {
    return () => {
      return h('div', { class: `${classses.vouterView} vouter-view scrollbar` }, [
        <RouteView />
      ])
    }
  },
})

export default BlankLayout