
export enum EnvType {
    /** 开发环境 */
    DEVELOPMENT = 'development',
    /** 测试环境 */
    TESTING = 'testing',
    /** 预发布环境 */
    STAGING = 'staging',
    /** 生产环境 */
    PRODUCTION = 'production'
}


/** 环境 */
export interface EnvStruct {
    id: number
    createTime: string
    /** 环境类型 */
    envType: EnvType
    /** 项目id */
    appId: string
    /** 自定义环境名称 */
    envName: string
    /** 描述 */
    envDesc?: string
}
