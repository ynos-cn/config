import { defineComponent, h, useSlots } from 'vue'
import { Table } from 'ant-design-vue'
import { tableProps } from './interface'
import { initDefaultProps } from '@/utils/initDefaultProps'

const BaseTable = defineComponent({
  name: 'BaseTable',
  props: initDefaultProps(tableProps(), {
    rowKey: 'id',
    size: "small"
  }),
  setup(props, { slots }) {

    return () => {
      return (
        h('div', { class: "base-table" }, [
          h(Table,
            { ...props as any, },
            { ...slots }
          )
        ])
      )
    }
  }
})

export default BaseTable
