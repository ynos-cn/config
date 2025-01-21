import { BaseParams, ResDataStruct } from "@/interface/base";
import { EnvStruct } from "@/interface/Env";
import { axios } from "@/utils/request";

/**
 *  查询全部
 */
export function apiFind(data: BaseParams<EnvStruct>) {
  return axios<ResDataStruct<Array<EnvStruct>>>({
    url: '/config/api/env/find',
    method: "POST",
    data
  })
}

/**
 *  查询详情
 */
export function apiFindWithID(id: string) {
  return axios<ResDataStruct<EnvStruct>>({
    url: '/config/api/env/id/' + id,
    method: "GET",
  })
}

/**
 *  新增
 */
export function apiSave(data: EnvStruct) {
  let url = '/config/api/env/create'
  if (data.id) {
    url = '/config/api/env/update'
  }
  return axios<ResDataStruct<EnvStruct>>({
    url,
    method: "POST",
    data
  })
}

/**
 *  删除
 */
export function apiDelete(data: Array<string>) {
  return axios({
    url: '/config/api/env/delete',
    method: "DELETE",
    data
  })
}
