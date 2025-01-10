/*
 * @Description: 基础布局
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-07-26 14:42:26
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2022-07-28 14:36:45
 */
import { defineComponent, h } from 'vue'
import { Layout, LayoutSider, LayoutContent } from 'ant-design-vue'
import RouteView from './route-view'
import GlobalHeader from './global-header/index'
import GlobalMenu from './global-menu/index';
import GlobalFooter from './global-footer/index'

import classses from './index.module.less'

const BasicLayout = defineComponent({
  name: 'BasicLayout',
  setup() {
    return () => {
      return (
        h(Layout, { class: `${classses.ZLayout} z-layout` }, () => [
          h(GlobalHeader),
          h(Layout, () => [
            h(LayoutSider, { width: 230, theme: 'light' }, () => [h(GlobalMenu)]),
            h(LayoutContent, () => [h(RouteView)])
          ]),
          h(GlobalFooter)
        ])
      )
    }
  }
})

export default BasicLayout