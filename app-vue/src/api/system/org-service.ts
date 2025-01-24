import { BaseParams, ResDataStruct } from "@/interface/base";
import { OrgStruct } from "@/interface/org";
import { axios } from "@/utils/request";

/**
 *  根据用户名查询所在机构
 */
export function queryOrgNameAPI(username: string) {
  return axios<ResDataStruct<any>>({
    url: '/ioa/api/sys/org/queryOrgName',
    method: "POST",
    data: {
      username
    }
  })
}

/**
 *  查询列表
 */
export function apiFind(data: BaseParams<OrgStruct>) {
  return axios<ResDataStruct<Array<OrgStruct>>>({
    url: '/ioa/api/sys/org/find',
    method: "POST",
    data
  })
}

/**
 *  查询全部机构
 */
export function apiAllFind() {
  return axios<ResDataStruct<Array<OrgStruct>>>({
    url: '/ioa/api/sys/org/findAll',
    method: "POST",
  })
}

/**
 *  查询详情
 */
export function apiFindWithID(id: number) {
  return axios<ResDataStruct<OrgStruct>>({
    url: '/ioa/api/sys/org/id/' + id,
    method: "GET",
  })
}
