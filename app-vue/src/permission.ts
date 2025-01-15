import router from "./router";
import { useAppStore } from '@/store/app'
import { useCancelTokenStore } from '@/store/cancelToken'
import NProgress from 'nprogress'
import "nprogress/nprogress.css";
import { setDocumentTitle } from './utils/domUtil';
import { getToken, goToLogin } from '@/utils/utils'

// 白名单列表
const whiteList: Array<string> = []

NProgress.configure({ showSpinner: false })


router.beforeEach((to, from, next) => {
  const appStore = useAppStore()
  const cancelTokenStore = useCancelTokenStore()

  NProgress.start()

  // 中断上一页的请求
  cancelTokenStore.removeHttpRequestMap()

  // token参数处理
  if (to.query.token || from.query.token) {
    appStore.setToken((to.query.token || from.query.token) as string)
  }
  if (from.query.isIframe) {
    to.query['isIframe'] = from.query.isIframe
  }

  // 设置标题
  to.meta && (typeof to.meta.title !== 'undefined' && setDocumentTitle(to))

  if (getToken()) {
    if (!appStore.userInfo) {
      appStore.isAuth().then(() => {
        next({ path: (to.fullPath ? to.fullPath : to.path) as any, query: to.query, params: to.params });
        NProgress.done()
      }).catch(() => {
        // 跳转到登录页面
        goToLogin()
        NProgress.done() // if current page is login will not trigger afterEach hook, so manually handle it
      })
      return;
    }

    // 如果url中携带了token  则直接放行并且删除url的token
    if (to.query.token) {
      delete to.query.token
      next({ path: (to.fullPath ? to.fullPath : to.path) as any, query: to.query, params: to.params })
      return
    }

    // 直接放行
    next();
    NProgress.done()
  } else {
    if (whiteList.includes(to.path)) {
      next()
      NProgress.done()
    } else {
      appStore.isAuth().then(() => {
        next({ path: (to.fullPath ? to.fullPath : to.path) as any, query: to.query, params: to.params })
      }).catch(() => {
        goToLogin()
        NProgress.done()
      })
    }
  }
})
