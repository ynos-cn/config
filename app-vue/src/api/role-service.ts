import { BaseParams, ResDataStruct } from "@/interface/base";
import { RoleStruct } from "@/interface/Role";
import { axios } from "@/utils/request";

/**
 *  查询全部
 */
export function apiFind(data: BaseParams<RoleStruct>) {
  return axios<ResDataStruct<Array<RoleStruct>>>({
    url: '/config/api/role/find',
    method: "POST",
    data
  })
}

/**
 *  查询详情
 */
export function apiFindWithID(id: string) {
  return axios<ResDataStruct<RoleStruct>>({
    url: '/config/api/role/id/' + id,
    method: "GET",
  })
}

/**
 *  新增
 */
export function apiSave(data: RoleStruct) {
  let url = '/config/api/role/create'
  if (data.id) {
    url = '/config/api/role/update'
  }
  return axios<ResDataStruct<RoleStruct>>({
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
    url: '/config/api/role/delete',
    method: "DELETE",
    data
  })
}
