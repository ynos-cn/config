import { BaseStruct } from "./base"

/** 角色 */
export interface ProjectStruct extends BaseStruct {
    /** 名称 */
    appName: string
    /** 项目id */
    appId?: string
    /** 项目管理员 */
    projectManagers: string | string[]
    /** 描述 */
    description?: string
    /** 配置拉取认证开关：0关闭 1：打开 */
    pullSwitch: number
    /** 多环境开关 */
    envSwitch: number
    /** 所属机构名称 */
    orgName: string
}
