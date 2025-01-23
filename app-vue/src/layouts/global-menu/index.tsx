/*
 * @Description: 菜单
 * @Version: 1.0
 */

import { defineComponent, h, ref, computed, watch } from 'vue'
import { RouteRecordRaw, useRouter, useRoute } from 'vue-router'
import { Menu, SubMenu, MenuItem } from 'ant-design-vue'

import classes from './index.module.less'
import { SelectInfo } from 'ant-design-vue/lib/menu/src/interface'
import { Key } from 'ant-design-vue/lib/_util/type'

const GlobalMenu = defineComponent({
  name: 'GlobalMenu',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const menus = router.options.routes[0].path === '/' && router.options.routes[0].name === 'index' && router.options.routes.length <= 1 ? router.options.routes[0].children || [] : router.options.routes;

    const selectedKeys = ref<Array<string>>([])
    const openKeys = ref<Array<Key>>([])

    const rootSubmenuKeys = computed(() => {
      const keys: Array<Key> = []
      menus.forEach(item => keys.push(item.path))
      return keys
    })

    const renderSubMenu = (menu: RouteRecordRaw) => {
      const childrenList: any = []
      menu.children?.map(e => childrenList.push(renderItem(e)))
      return (
        h(SubMenu, { ...{ key: menu.path, title: menu.meta?.title } }, () => [
          childrenList
        ])
      )
    }

    const renderMenuItem = (menu: RouteRecordRaw) => {
      return (
        h(MenuItem, { ...{ key: menu.path } }, () => [
          menu.meta?.title || ''
        ])
      )
    }

    const renderItem = (menu: RouteRecordRaw) => {
      if (menu.meta?.hidden) {
        return null
      }
      return menu.children ? renderSubMenu(menu) : renderMenuItem(menu)
    }

    const renderMenuTree = () => {
      return menus.filter(e => !e.meta?.hidden).map(v => {
        return renderItem(v)
      })
    }

    const updateMenu = () => {
      const routes = route.matched.concat()
      if (routes.length >= 4 && route.meta.hidden) {
        routes.pop()
        selectedKeys.value = [routes[2].path]
      } else {
        selectedKeys.value = [routes.pop()?.path ?? '']
      }
      openKeys.value = []
      routes.map(v => {
        openKeys.value.push(v.path)
      })
    }

    /** 菜单点击事件 */
    const menuSelect = (record: SelectInfo) => {
      selectedKeys.value = record.selectedKeys as Array<string>
      router.push(record.key as string)
    }

    /** 菜单 	SubMenu 展开/关闭的回调 */
    const menuOpenChange = (keys: Array<Key>) => {
      const latestOpenKey = keys.find(key => !openKeys.value.includes(key))
      if (latestOpenKey && !rootSubmenuKeys.value.includes(latestOpenKey)) {
        openKeys.value = keys
      } else {
        openKeys.value = latestOpenKey ? [latestOpenKey] : []
      }
    }


    watch(() => route, () => {
      updateMenu()
    }, { immediate: true, deep: true })

    return () => {
      return h('div', { class: `${classes.globalMenu} scrollbar` }, [
        h(Menu, {
          style: { height: '100%' },
          mode: 'inline',
          selectedKeys: selectedKeys.value,
          openKeys: openKeys.value,
          onSelect: menuSelect,
          onOpenChange: menuOpenChange,
        }, () => [renderMenuTree()])
      ])
    }
  }
})

export default GlobalMenu
