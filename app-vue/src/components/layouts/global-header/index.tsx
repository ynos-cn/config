/*
 * @Description: 头部
 * @Version: 1.0
 * @Autor: jiajun.wu
 */
import { defineComponent, h } from 'vue'
import classes from './index.module.less'
import { ExclamationCircleOutlined, LogoutOutlined } from '@ant-design/icons-vue'
import { useAppStore } from '@/store/app'
import { Modal } from 'ant-design-vue'

const globalHeader = defineComponent({
  name: 'GlobalHeader',
  setup(_props) {
    const headerIcon = () => {
      return (
        h('div', { class: classes.logo }, [])
      )
    }

    const appStore = useAppStore()

    const logout = () => {
      const onclick = () => {
        Modal.confirm({
          title: '确认消息',
          icon: h(ExclamationCircleOutlined),
          content: '确定要关闭？',
          okText: '确认',
          cancelText: '取消',
          onOk: () => {
            appStore.logout().finally(() => {
              location.reload();
            })
          }
        });
      }
      return (
        h('div', { class: classes.logout, title: '退出登录', onclick }, [h(LogoutOutlined)])
      )
    }

    const userInfo = () => {
      return (
        h('div', { class: classes.userInfo }, [appStore.userInfo?.name])
      )
    }

    return () => {
      return h('div', { class: classes.globalHeader }, [
        headerIcon(),
        userInfo(),
        logout()
      ])
    }
  }
})

export default globalHeader
