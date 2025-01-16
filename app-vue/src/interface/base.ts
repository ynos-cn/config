import { UserStruct } from "./user"

/** 基础api请求类型 */
export interface BaseParams<T = any> {
  body?: T
  /** 当前页,示例值(1) */
  page?: number
  /** 分页大小, 示例值(10) */
  limit?: number
  /** 默认升序（1为升序，-1为降序）   */
  sorter?: {
    [key: string]: number
  }
}

/** 验证响应 */
export interface AuthResStruct {
  /** 响应内容体 */
  data: UserStruct,
  /** api响应信息 */
  msg: string,
  /** api接口返回是否成功 */
  success: boolean,
  token: string
}

/** 普通数据响应 */
export interface ResDataStruct<T = any> {
  /** 响应内容体 */
  data: T,
  /** api响应信息 */
  msg: string,
  /** api响应编码 */
  code: number,
  /** 当前请求页数 */
  page: number,
  /** 内容最大限制 */
  limit: number,
  /** api接口返回是否成功 */
  success: boolean,
  /** api接口查询数据库总数 */
  total: number,
}

/**
 * 基础数据结构
 */
export interface BaseStruct {
  /** 唯一id */
  id?: string | number
  /** 创建人 */
  creator?: string
  /** 创建时间 */
  createTime?: string
  /** 更新时间 */
  updateTime?: string
  /** 更新人 */
  updater?: string
  /** 所属机构id */
  orgId?: string
}

/** 返回上一页数据 */
export interface GoBackData {
  url: string
  /** 搜索条件 */
  searchData?: {
    [key: string]: any
  }
  pagination?: {
    current?: number
    pageSize?: number
  }
  sorter?: {
    [key: string]: number
  }
  [key: string]: any
}

/**
 * 分页配置
 */
export interface Pagination {
  total: number;
  current: number;
  pageSize: number;
  showTotal: (total: number) => string;
  pageSizeOptions: string[];
  showSizeChanger: boolean;
  onShowSizeChange: (_: any, _pageSize: any) => any;
}
