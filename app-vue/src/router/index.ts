import { BasicLayout, UserLayout } from '@/components/layouts'
import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router"

const routers: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'index',
    component: BasicLayout,
    meta: { title: '配置中心' },
    redirect: '/home',
    children: [
      {
        path: '/home',
        name: 'home',
        component: () => import('@/views/project/index.vue'),
        meta: { title: '配置中心' }
      },
    ],
  },
  {
    path: '/login',
    component: UserLayout,
    redirect: '/login/login',
    meta: {
      title: "登录",
      hidden: true,
    },
    children: [
      {
        path: '/login/login',
        name: 'login',
        component: () => import('@/views/login/login.vue'),
        meta: { title: '登录' }
      },
      {
        path: '/login/register',
        name: 'register',
        component: () => import('@/views/login/Register.vue'),
        meta: { title: '注册' }
      },
    ]
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
  history: createWebHashHistory(),
  routes: routers as RouteRecordRaw[]
})

router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  let title = to.meta.title ?? '首页';
  document.title = title as string
  next()
})

export default router;
