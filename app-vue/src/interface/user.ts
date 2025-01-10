import { Dayjs } from "dayjs"
import { BaseStruct } from "./base"

/** 用户 */
export interface UserStruct extends BaseStruct {
    /** 名称 */
    name: string
    /** 手机号码 */
    phone: string
    /** 职位 */
    position?: string
    /** 入职时间 */
    joinTime?: string | Dayjs
    /** 性别 1.男 0.女 */
    sex?: number
    /** 邮箱 */
    email?: string
    /** 所属机构名称 */
    orgName?: string
    /** 状态 0.禁用 1.可用 */
    status: number
}
