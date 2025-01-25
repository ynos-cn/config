/** 权限类型 */
export const PermissionTypeList = [
  { name: 'PERMISSION_LOOK', label: '只读', value: 1, type: 1 },
  { name: 'PERMISSION_ADD', label: '添加配置', value: 2, type: 2 },
  { name: 'PERMISSION_UPDATE', label: '修改配置', value: 3, type: 2 },
  { name: 'PERMISSION_DELETE', label: '删除配置', value: 4, type: 2 },
  { name: 'PERMISSION_CREATE_TASK', label: '提交发布', value: 8, type: 2 },
  { name: 'PERMISSION_APPROVE_TASK', label: '审批发布(固定审批人)', value: 11, type: 2 },
  { name: 'PERMISSION_RELEASE_TASK', label: '执行发布', value: 10, type: 2 },
  { name: 'PERMISSION_RELEASE', label: '管理分组', value: 6, type: 3 },
]


export enum PermissionTypeEnum {
  PERMISSION_LOOK = 1, // 只读
  PERMISSION_ADD = 2, // 添加配置
  PERMISSION_UPDATE = 3, // 修改配置
  PERMISSION_DELETE = 4, // 删除配置
  PERMISSION_CREATE_TASK = 8, // 提交发布
  PERMISSION_APPROVE_TASK = 11, // 审批发布(固定审批人)
  PERMISSION_RELEASE_TASK = 10, // 执行发布
  PERMISSION_RELEASE = 6, // 管理分组
}
