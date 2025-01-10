/*
 * @Description: 路由配置
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2023-08-04 10:28:53
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2024-01-16 15:44:27
 */
import { BasicLayout, UserLayout } from '@/components/layouts'
import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router"

const routers: Array<RouteRecordRaw> = [
  // {
  //   path: '/',
  //   name: 'index',
  //   component: BasicLayout,
  //   meta: { title: '首页' },
  //   children: [
  //   ],
  // },
  {
    path: '/',
    name: 'system',
    component: BasicLayout,
    meta: { title: '系统管理' },
    redirect: '/org',
    children: [
      {
        path: '/org',
        name: 'org',
        component: () => import('@/views/system/org/manage.vue'),
        meta: { title: '机构管理' }
      },
      {
        path: '/role',
        name: 'role',
        component: () => import('@/views/system/role/manage.vue'),
        meta: { title: '角色管理' }
      },
      {
        path: '/users',
        name: 'users',
        component: () => import('@/views/system/users/manage.vue'),
        meta: { title: '员工管理' }
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: UserLayout,
    // redirect: '/login',
    meta: {
      title: "登录",
      hidden: true,
    },
    children: [
      {
        path: '/login',
        name: 'login',
        component: () => import('@/views/login/index.vue'),
        meta: { title: '登录' }
      },
      {
        path: 'register',
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
