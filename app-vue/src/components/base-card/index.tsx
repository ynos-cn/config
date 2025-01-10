/*
 * @Description: 基础卡片
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-07-28 10:37:13
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-03-31 16:21:16
 */
import { defineComponent, ref, h, watch, useSlots, PropType } from 'vue'
import { useRoute } from 'vue-router'
import classes from './index.module.less'
import { RollbackOutlined } from '@ant-design/icons-vue'

const BaseCard = defineComponent({
  name: 'BaseCard',
  props: {
    /** 标题 */
    title: {
      type: String as PropType<any>
    },
    /** 返回按钮 */
    goBack: {
      type: Boolean,
    },
    'onBack': Function as PropType<(event?: PointerEvent) => void>
  },
  emits: ['back'],
  setup(props, { emit }) {
    const route = useRoute()

    /** 卡片标题 */
    const cardTitle = ref<string>(props?.title || route.meta.title || '')
    const slots = useSlots()
    /** 内容渲染器 */
    const renderBody = () => {
      if (!slots.default) {
        return
      }
      return (
        h('div', { class: `${classes.baseCardBody} base-card-body` }, [
          slots.default()
        ])
      )
    }

    /** 标题右侧渲染器 */
    const renderTitleRight = () => {
      if (!slots.addonAfter && !props.goBack) {
        return
      }
      return (
        h('div', { class: `${classes.addonAfter} title-right` }, [
          !slots.addonAfter ?
            h(RollbackOutlined, { style: { cursor: 'pointer' }, onClick: (e: any) => { emit('back', e) } }) :
            slots.addonAfter(cardTitle.value)
        ])
      )
    }

    /** 渲染标题 */
    const renderTitle = () => {
      if (props.title === null) {
        return
      }

      return (
        h('div', { class: `${classes.baseCardTitle} base-card-title` }, [
          h('div', { class: `${classes.hl} base-card-title-hl` }),
          cardTitle.value,
          renderTitleRight()
        ])
      )
    }

    watch(() => props.title, (val) => {
      if (val) {
        cardTitle.value = val
      }
    })

    return () => {
      return (
        h('div', { class: `${classes.baseCard} base-card` }, [
          renderTitle(),
          renderBody()
        ])
      )
    }
  }
})

export default BaseCard