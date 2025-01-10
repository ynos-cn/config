import { BaseStruct } from "./base"

/** 机构 */
export interface OrgStruct extends BaseStruct {
    /** 名称 */
    name: string
    /** 机构代码 */
    code: string
    /** 负责人名称 */
    controllerName: string
    /** 负责人联系电话 */
    controllerTel: string
    /** 所属机构 */
    orgName?: string
    [key: string]: any
}
