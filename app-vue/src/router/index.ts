import { BasicLayout } from '@/components/layouts'
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

const routers: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'index',
    component: BasicLayout,
    meta: { title: '配置中心' },
    redirect: '/console',
    children: [
      {
        path: '/console',
        name: 'console',
        component: () => import('@/views/project/index.vue'),
        meta: { title: '配置中心' }
      },
      {
        path: '/:id',
        name: 'config',
        component: () => import('@/views/config/index.vue'),
        meta: { title: '配置中心' },
        children: [
          {
            path: '/:id/list',
            name: 'list',
            component: () => import('@/views/config/list/index.vue'),
            meta: { title: '配置中心' }
          },
        ]
      },
    ],
  },
  {
    path: '/:pathMatch(.*)',
    name: '404',
    component: () => import('@/views/exception/404.vue'),
    meta: {
      title: '404',
      hidden: true
    }
  },
];

const router = createRouter({
  history: createWebHistory('config'),
  routes: routers as RouteRecordRaw[]
})

router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  let title = to.meta.title ?? '首页';
  document.title = title as string
  next()
})

export default router;
