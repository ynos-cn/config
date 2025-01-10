/*
 * @Description: 高级搜索表单
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-08-19 14:17:20
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-03-29 11:57:06
 */
import { ref, defineComponent, PropType, h, Ref, useSlots, watch } from 'vue'
import { Input, Button, Dropdown, CheckboxGroup, Menu, MenuItem, Checkbox } from 'ant-design-vue'
import { SearchOutlined, ReloadOutlined, FilterOutlined } from '@ant-design/icons-vue'
import Dynamic from './dynamic.vue'
import classses from './index.module.less'
import './index.less'
import { SearchConfig } from './interface'
import dayjs from 'dayjs'

const BaseSearch = defineComponent({
  name: 'BaseSearch',
  props: {
    /** 高级选项配置 */
    config: {
      type: Array as PropType<Array<SearchConfig>>,
      default: () => [],
    },
    /** 是否关闭关键字搜索 */
    isNoKeywords: {
      type: Boolean,
      default: () => false,
    },
    /** 关键字搜索提示 */
    keywordsPlaceholder: {
      type: String,
      default: () => '关键字搜索',
    },
    /** 初始化数据 */
    initSearchData: {
      type: Object as PropType<{ [key: string]: any }>,
    },
    onReset: Function,
    onSearch: Function as PropType<(queryData?: any) => void>
  },
  setup(props, { }) {
    const keywords = ref('')
    const onKeyUp = (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        doQuery()
      }
    };
    // 关键字搜索
    const inputKeywords = (e: any) => {
      keywords.value = e?.target?.value ?? ''
    }
    const keyWordInput = () => {
      if (props.isNoKeywords) {
        return
      }
      return h(Input, { class: classses.keywordInput, placeholder: props.keywordsPlaceholder ?? '关键字搜索', onkeyup: onKeyUp, value: keywords.value, onInput: inputKeywords })
    }

    const queryData: Ref<any> = ref({})
    const checkedValues = ref<Array<string>>([])
    function doQuery() {
      let data: any = {
        keywords: keywords.value,
      }
      checkedValues.value.map(key => {
        data[key] = queryData.value[key]
      })
      if (props.onSearch) {
        props.onSearch(data)
      }
    }

    /** 重置 */
    function handleReset() {
      queryData.value = {}
      checkedValues.value = props.config.filter(e => e.defaultShow).map(e => e.key)
      keywords.value = ''
      if (props.onReset) {
        props.onReset()
      }
      if (props.onSearch) {
        props.onSearch()
      }
    }

    /** 方法按钮事件 */
    const funBtn = () => {
      return h('div', { class: classses.funBtn }, [
        h(Button, { class: classses.searchButton, onClick: doQuery }, () => [h(SearchOutlined), '查询']),
        funConfig(),
        h(Button, { class: classses.searchButton, onClick: handleReset }, () => [h(ReloadOutlined), '重置']),
      ])
    }

    /** 高级搜索按钮项 */
    const funConfig = () => {
      if (props.config.length <= 0) {
        return
      }
      /** 高级搜索控件选择事件 */
      const checkboxChange = (e: any) => {
        checkedValues.value = e

        for (let key in queryData.value) {
          if (checkedValues.value.findIndex((v) => v == key) <= -1) {
            delete queryData.value[key]
          }
        }
      }

      const overlayRender = () => {
        return h('div', { class: 'search-config-box scrollbar' }, [h(CheckboxGroup, { value: checkedValues.value, onChange: checkboxChange }, () => [
          h(Menu, () => [
            props.config.map(v => {
              return h(MenuItem, { key: v.key }, () => [h(Checkbox, { value: v.key }, () => [v.label])])
            })
          ])
        ])])
      }
      return h(Dropdown, { class: classses.searchButton, overlay: overlayRender() }, () => [h(Button, () => [h(FilterOutlined), '高级搜索'])])
    }

    const slots = useSlots()
    const renderSlot = (record: SearchConfig) => {

      if ((slots as any)[record.key]) {
        return (slots as any)[record.key]()
      } else {
        return h(Dynamic, {
          class: `base-search-dynamic-${record.key}`,
          attrs: {
            ...record.attrs,
            placeholder: ['a-range-picker'].includes(record.type) ? ['开始时间', '结束时间'] : record?.attrs?.placeholder ?? `${record.label}搜索`
          },
          style: { width: '100%' },
          component: record.type,
          value: ['a-range-picker'].includes(record.type) ? queryData.value[record.key]?.length > 1 ? [dayjs(queryData.value[record.key][0]), dayjs(queryData.value[record.key][1])] : undefined : queryData.value[record.key],
          onChange: record.onChange ? record.onChange : (event: any) => {
            queryData.value[record.key] = event?.target?.value ?? event ?? ''
          },
        })
      }
    }

    /** 初始默认展示 */
    watch(() => props.config, () => {
      checkedValues.value = props.config.filter(e => e.defaultShow).map(e => e.key)
    }, { immediate: true })

    /** 设置初始化搜索参数 */
    const setSearchData = (data: { [key: string]: any }) => {
      for (const key in data) {
        if (Object.prototype.hasOwnProperty.call(data, key)) {
          if (key === 'keywords') {
            keywords.value = data[key]
          } else {
            let index = checkedValues.value.findIndex(e => e === key)
            if (index <= -1) {
              checkedValues.value.push(key)
            }
            queryData.value[key] = data[key]
          }
        }
      }
    }
    watch(() => props.initSearchData, (val) => {
      if (val) {
        setSearchData(val)
      }
    }, { immediate: true })

    /** 动态渲染组件 */
    const dynamicRenderC = () => {
      return checkedValues.value.map(k => {
        let item = props.config.find(e => e.key === k)
        if (item) {
          return h('div',
            {
              class: `${classses.dynamicDiv} ${item.showLabel && classses.showLabelDynamicDiv}`,
              key: k,
              style: { width: item?.width ?? '200px', ...item?.attrs?.style }
            },
            [
              item.showLabel ? `${item.label}：` : undefined,
              renderSlot(item),
            ])
        }
      })
    }

    return () => h('div', { class: classses.search }, [keyWordInput(), dynamicRenderC(), funBtn()])
  }
})

export default BaseSearch