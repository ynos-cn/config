import { defineComponent, h } from 'vue'
import { Layout, LayoutContent } from 'ant-design-vue'
import RouteView from './route-view'
import GlobalHeader from './global-header/index'
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
            h(LayoutContent, () => [h(RouteView)])
          ]),
          h(GlobalFooter)
        ])
      )
    }
  }
})

export default BasicLayout
