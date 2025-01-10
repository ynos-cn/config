/*
 * @Description: 接口定义
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-08-08 14:05:35
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-03-29 18:55:41
 */

export interface SearchConfig {
  /** 控件类型 */
  type: string;
  /** 类型key */
  key: string;
  /** 条件名称 */
  label: string;
  /** 是否展示label */
  showLabel?: boolean;
  width?: string | number;
  attrs?: any,
  /** 是否默认展示 */
  defaultShow?: boolean;
  [key: string]: any
}