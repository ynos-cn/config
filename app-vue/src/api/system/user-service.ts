import { BaseParams, ResDataStruct } from "@/interface/base";
import { UserStruct } from "@/interface/user";
import { axios } from "@/utils/request";

/**
 *  查询全部
 */
export function apiFind(data: BaseParams<UserStruct>) {
  return axios<ResDataStruct<Array<UserStruct>>>({
    url: '/api/sys/user/find',
    method: "post",
    data
  })
}

/**
 *  新增
 */
export function apiSave(data: UserStruct) {
  let url = '/api/sys/user/create'
  if (data.id) {
    url = '/api/sys/user/update'
  }
  return axios<ResDataStruct<UserStruct>>({
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
    url: '/api/sys/user/delete',
    method: "delete",
    data
  })
}
