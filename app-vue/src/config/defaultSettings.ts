/*
 * @Description: 项目默认配置项
 * @Version: 1.0
 * @Autor: jiajun wu
 * @Date: 2022-04-12 14:59:01
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2022-07-28 10:36:02
 */
export default {
  storageOptions: {
    namespace: 'pro__', // key prefix
    name: 'ls', // name variable Vue.[ls] or this.[$ls],
    storage: 'local' // storage name session, local, memory
  },
  systemName: 'portal',
  context: import.meta.env.VITE_APP_CONTEXT as string || '',
}