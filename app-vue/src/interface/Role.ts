
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
    [key: string]: any
}

export interface Person {
    /** 名称 */
    names?: string
    /** 组织/机构ID */
    orgIds?: string
    /** 角色类型，1、OA帐号；2、机构 */
    type?: number
}

/** 自定义用户 */
export interface CustomUser {
    userName?: string
    userId?: string
    secretKey?: string
    enableStatus?: number
    [key: string]: any
}
