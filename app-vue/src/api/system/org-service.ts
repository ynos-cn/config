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
