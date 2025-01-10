import { BaseStruct } from "./base"

/** 角色 */
export interface RoleStruct extends BaseStruct {
    /** 名称 */
    name: string
    /** 角色代码 */
    code: string
    /** 描述 */
    describe: string
}
