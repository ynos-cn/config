import { BaseParams, ResDataStruct } from "@/interface/base";
import { RoleStruct } from "@/interface/role";
import { axios } from "@/utils/request";

/**
 *  查询全部
 */
export function apiFind(data: BaseParams<RoleStruct>) {
  return axios<ResDataStruct<Array<RoleStruct>>>({
    url: '/api/sys/role/find',
    method: "post",
    data
  })
}

/**
 *  新增
 */
export function apiSave(data: RoleStruct) {
  let url = '/api/sys/role/create'
  if (data.id) {
    url = '/api/sys/role/update'
  }
  return axios<ResDataStruct<RoleStruct>>({
    url,
    method: "post",
    data
  })
}

/**
 *  删除
 */
export function apiDelete(data: Array<string>) {
  return axios({
    url: '/api/sys/role/delete',
    method: "delete",
    data
  })
}
