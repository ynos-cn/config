import router from "./router";
import { useAppStore } from '@/store/app'
import { useCancelTokenStore } from '@/store/cancelToken'
import NProgress from 'nprogress'
import "nprogress/nprogress.css";
import { setDocumentTitle } from './utils/domUtil';
import { getToken } from '@/utils/utils'

// 白名单列表
const whiteList = ["/login", "/register", '/login/login', '/login/register', "/web/#/login", "/web/#/register"]

NProgress.configure({ showSpinner: false })


router.beforeEach((to, from, next) => {
  const appStore = useAppStore()
  const cancelTokenStore = useCancelTokenStore()

  NProgress.start()
  // 中断上一页的请求
  cancelTokenStore.removeHttpRequestMap()
  if (to.path === '/login/login') {
    next()
    NProgress.done()
  }
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
    // 如果已认证，并且又请求登录页面，则返回首页
    if (to.path === '/login/login') {
      next({ path: '/' })
      NProgress.done()
      return;
    }

    if (!appStore.userInfo) {
      appStore.isAuth().then(() => {
        next({ path: (to.fullPath ? to.fullPath : to.path) as any, query: to.query, params: to.params });
        NProgress.done()
      }).catch(() => {
        // 跳转到登录页面
        next({ path: '/login/login' })
        NProgress.done() // if current page is login will not trigger afterEach hook, so manually handle it
      })
      return;
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
        next("/login/login")
        NProgress.done()
      })
    }
  }
})
