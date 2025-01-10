/*
 * @Description: 
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-08-29 14:35:58
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2022-08-30 16:48:55
 */
import { PropType } from 'vue'
import { TableProps } from "ant-design-vue/lib/vc-table/Table";
import { TablePaginationConfig, tableProps as tP } from 'ant-design-vue/lib/table'
import { Column } from '@/interface/table';
import { SpinProps } from 'ant-design-vue/lib/spin';

export function tableProps() {
  return {
    ...tP(),
    dataSource: {
      type: Array as PropType<TableProps<any>['data']>,
      default: undefined
    },
    columns: {
      type: Array as PropType<Array<Column<any>> | any>,
      default: undefined
    },
    loading: {
      type: [Boolean, Object] as PropType<Boolean | SpinProps>,
      default: undefined
    },
    pagination: {
      type: [Boolean, Object] as PropType<Boolean | TablePaginationConfig>,
      default: undefined,
    },
    rowSelection: {
      type: Object as any,
      default: undefined
    },
  }
}

export default tableProps