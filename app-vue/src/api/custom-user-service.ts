import { BaseParams, ResDataStruct, CustomUser } from "@/interface";
import { axios } from "@/utils/request";

/**
 *  查询全部
 */
export function apiFind(data: BaseParams<CustomUser>) {
  return axios<ResDataStruct<Array<CustomUser>>>({
    url: '/config/api/customUser/find',
    method: "POST",
    data
  })
}

/**
 *  查询详情
 */
export function apiFindWithID(id: string) {
  return axios<ResDataStruct<CustomUser>>({
    url: '/config/api/customUser/id/' + id,
    method: "GET",
  })
}

/**
 *  新增
 */
export function apiSave(data: CustomUser) {
  let url = '/config/api/customUser/create'
  return axios<ResDataStruct<CustomUser>>({
    url,
    method: "POST",
    data
  })
}

/**
 *  更新状态
 */
export function updateStatus(data: CustomUser) {
  let url = '/config/api/customUser/updateStatus'
  return axios<ResDataStruct<CustomUser>>({
    url,
    method: "POST",
    data
  })
}



/**
 *  删除
 */
export function apiDelete(data: Array<string>) {
  return axios<ResDataStruct<number>>({
    url: '/config/api/customUser/delete',
    method: "DELETE",
    data
  })
}
