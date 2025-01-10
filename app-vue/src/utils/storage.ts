/*
 * @Description: 存储
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-07-26 15:05:21
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-08-01 11:54:45
 */
import { Storage, sessionStorage } from "ynos-storage";
import Cookies from "js-cookie";

/** 本地存储  LocalStorage */
export const LocalStorage = Storage.useStorage({
  namespace: "pro__",
}).ls;
/** 本地会话  SessionStorage */
export const SessionStorage = sessionStorage.useStorage();
// /** Cookie  Cookie */
export const Cookie = Cookies;
