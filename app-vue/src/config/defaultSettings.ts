/*
 * @Description: 项目默认配置项
 * @Version: 1.0
 */
export default {
  storageOptions: {
    namespace: 'pro__', // key prefix
    name: 'ls', // name variable Vue.[ls] or this.[$ls],
    storage: 'local' // storage name session, local, memory
  },
  systemName: 'portal',
  context: import.meta.env.VITE_APP_CONTEXT as string || '',
  loginUrl: '/ioa/login/login',
}
