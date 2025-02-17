import { isAuthed, logout as logoutApi } from '@/api/system-service'
import { getQueryVariable, setToken as uSetToken, getToken as uGetToken } from '@/utils/utils'
import { notification } from 'ant-design-vue'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { UserStruct } from '@/interface/user'

export const useAppStore = defineStore('app', () => {
  /** 登录token */
  const appToken = ref<string>()
  /** 用户信息 */
  const userInfo = ref<UserStruct>()

  /** 设置token ======================================== */
  const setToken = (token: string) => {
    uSetToken(token)
    appToken.value = token
  }
  const getToken = () => {
    const token = getQueryVariable("token") || uGetToken()
    appToken.value = token
    return appToken.value
  }
  /** 设置token ======================================== */

  /** 验证是否已登录 */
  const isAuth = () => {
    return new Promise((resolve, reject) => {
      const token = getToken()
      if (token) {
        isAuthed()
          .then((res: any) => {
            if (res.success) {
              userInfo.value = res.data
              setToken(res.token)
              resolve(res.data)
            } else {
              userInfo.value = undefined
              setToken('')
              reject()
            }
          }).catch(() => {
            userInfo.value = undefined
            setToken('')
            reject()
          })
      } else {
        userInfo.value = undefined
        setToken('')
        reject()
      }
    })
  }

  const logout = () => {
    return new Promise((resolve) => {
      const fn = () => {
        userInfo.value = undefined
        setToken('')
      }
      logoutApi().finally(() => {
        fn()
        resolve(true)
      })
    })
  }

  return {
    appToken,
    userInfo,
    isAuth,
    setToken,
    getToken,
    logout
  }
})
