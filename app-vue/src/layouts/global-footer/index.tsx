/*
 * @Description: 底部
 * @Version: 1.0
 */

import { defineComponent, h } from 'vue'
import { CopyrightOutlined } from '@ant-design/icons-vue'
import classes from './index.module.less'
import dayjs from 'dayjs'

const GlobalFooter = defineComponent({
  name: 'GlobalFooter',
  setup() {
    return () => {
      return (
        h('div', { class: classes.footer }, [
          "版权所有",
          h('span', { class: classes.icon }, [
            h(CopyrightOutlined),
            dayjs().format(' YYYY'),
          ]),
          " 由 jiajun wu 提供"
        ])
      )
    }
  }
})

export default GlobalFooter
