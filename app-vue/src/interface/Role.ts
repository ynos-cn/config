
/** 角色 */
export interface RoleStruct {
    /** id */
    id?: number
    /** 项目ID */
    appId?: string
    /** 环境列表 */
    envNames?: string[]
    /** 角色名 */
    name?: string
    /** 分组 */
    object?: string
    /** 权限类型 */
    permissionTypes?: string[]
    /** 人员列表 */
    persons?: Person[]
}


export interface Person {
    /** 名称 */
    names?: string
    /** 组织/机构ID */
    orgId?: number
    /** 角色类型，1、OA帐号；2、机构 */
    type?: number
}
