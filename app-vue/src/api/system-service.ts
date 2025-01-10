/*
 * @Description: 系统服务api
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-07-26 14:59:08
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-04-03 10:36:50
 */
import { AuthResStruct } from "@/interface/base";
import { axios } from "@/utils/request";

/**
 *  验证是否已登陆
 */
export function isAuthed() {
  return axios<AuthResStruct>({
    url: '/api/login/isAuth',
    method: "post"
  })
}

/**
 *  登录
 */
export function login(data: object) {
  return axios({
    url: '/api/login/login',
    method: "post",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    data
  })
}

/**
 *  退出登录
 */
export function logout() {
  return axios({
    url: '/api/login/logout',
    method: "post"
  })
}
