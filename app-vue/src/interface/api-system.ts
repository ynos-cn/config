/*
 * @Description: 
 * @Version: 1.0
 * @Autor: jiajun wu
 * @Date: 2022-07-09 10:56:21
 * @LastEditors: jiajun wu
 * @LastEditTime: 2022-07-14 14:42:46
 */
/** 行政区数据结构 */
export interface BaseAreaStruct {
  address: null | string
  alias: null | string
  appId: null | string
  en: string
  lat: null | string
  lng: null | string
  lockCode: null | string
  name: string
  parentId: string
  sid: string
  sn: string
  status: number
  types: number
}

/** 字典数据结构 */
export interface BaseDictStruct {
  appId: string | null
  appName: string | null
  created: string
  createdBy: string
  dictKey: string
  dictName: string
  dictType: number
  dictValue: string
  isLeaf: number
  parentId: string
  sid: string
  status: number | null
  tenantId: string
  userId: string | null
  ordered: number | null
}


/** 全局类型 */
export interface GlobalTypeStruct {
  value: string,
  label: string,
  [key: string]: any
}