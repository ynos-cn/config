/** 权限类型 */
export const PermissionType = [
  { name: 'PERMISSION_LOOK', label: '只读', value: 1, type: 1 },
  { name: 'PERMISSION_ADD', label: '添加配置', value: 2, type: 2 },
  { name: 'PERMISSION_UPDATE', label: '修改配置', value: 3, type: 2 },
  { name: 'PERMISSION_DELETE', label: '删除配置', value: 4, type: 2 },
  { name: 'PERMISSION_CREATE_TASK', label: '提交发布', value: 8, type: 2 },
  { name: 'PERMISSION_APPROVE_TASK', label: '审批发布(固定审批人)', value: 11, type: 2 },
  { name: 'PERMISSION_RELEASE_TASK', label: '执行发布', value: 10, type: 2 },
  { name: 'PERMISSION_RELEASE', label: '管理分组', value: 6, type: 3 },
]
