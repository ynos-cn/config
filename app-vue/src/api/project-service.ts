import { BaseParams, ResDataStruct } from "@/interface/base";
import { ProjectStruct } from "@/interface/Project";
import { axios } from "@/utils/request";

/**
 *  查询全部
 */
export function apiFind(data: BaseParams<ProjectStruct>) {
  return axios<ResDataStruct<Array<ProjectStruct>>>({
    url: '/config/api/project/find',
    method: "POST",
    data
  })
}

/**
 *  查询详情
 */
export function apiFindWithID(id: string) {
  return axios<ResDataStruct<ProjectStruct>>({
    url: '/config/api/project/id/' + id,
    method: "GET",
  })
}

/**
 *  新增
 */
export function apiSave(data: ProjectStruct) {
  let url = '/config/api/project/create'
  if (data.id) {
    url = '/config/api/project/update'
  }
  return axios<ResDataStruct<ProjectStruct>>({
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
    url: '/config/api/project/delete',
    method: "DELETE",
    data
  })
}
