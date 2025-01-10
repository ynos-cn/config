import { BaseParams, ResDataStruct } from "@/interface/base";
import { OrgStruct } from "@/interface/org";
import { axios } from "@/utils/request";

/**
 *  查询全部
 */
export function apiFind(data: BaseParams<OrgStruct>) {
  return axios<ResDataStruct<Array<OrgStruct>>>({
    url: '/api/sys/org/find',
    method: "POST",
    data
  })
}

/**
 *  查询详情
 */
export function apiFindWithID(id: string) {
  return axios<ResDataStruct<OrgStruct>>({
    url: '/api/sys/org/id/' + id,
    method: "GET",
  })
}

/**
 *  新增
 */
export function apiSave(data: OrgStruct) {
  let url = '/api/sys/org/create'
  if (data.id) {
    url = '/api/sys/org/update'
  }
  return axios<ResDataStruct<OrgStruct>>({
    url,
    method: "POST",
    data
  })
}


/**
 *  修改所属机构组织
 */
export function apiUpdateOrg(data: { id: string, orgId: string, orgName: string }) {
  return axios<ResDataStruct<OrgStruct>>({
    url: '/api/sys/org/updateOrg',
    method: "POST",
    data
  })
}

/**
 *  删除
 */
export function apiDelete(data: Array<string>) {
  return axios({
    url: '/api/sys/org/delete',
    method: "DELETE",
    data
  })
}
