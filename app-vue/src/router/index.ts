import { BasicLayout } from '@/components/layouts'
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router"

const routers: Array<RouteRecordRaw> = [
  {
    path: "/",
    redirect: "/config/console",
  },
  {
    path: '/config',
    name: 'index',
    component: BasicLayout,
    meta: { title: '配置中心' },
    redirect: '/config/console',
    children: [
      {
        path: '/config/console',
        name: 'console',
        component: () => import('@/views/project/index.vue'),
        meta: { title: '配置中心' }
      },
      {
        path: '/config/:id/:env',
        name: 'config',
        component: () => import('@/views/config/index.vue'),
        meta: { title: '配置中心' },
        children: [
          {
            path: '/config/:id/:env/base',
            name: 'base',
            component: () => import('@/views/config/base/index.vue'),
            meta: { title: '信息' }
          },
          {
            path: '/config/:id/:env/list',
            name: 'list',
            component: () => import('@/views/config/list/index.vue'),
            meta: { title: '配置中心' }
          },
          {
            path: '/config/:id/:env/task',
            name: 'task',
            component: () => import('@/views/config/task/index.vue'),
            meta: { title: '任务' }
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
  history: createWebHistory(),
  routes: routers as RouteRecordRaw[]
})

router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  let title = to.meta.title ?? '首页';
  document.title = title as string
  next()
})

export default router;
