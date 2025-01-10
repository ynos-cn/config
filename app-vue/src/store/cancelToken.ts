import { defineStore } from 'pinia'
import { Canceler } from 'axios'

export interface CancelTokenState {
  httpRequestMap: Map<string, Canceler>,
}
export interface ReqObj {
  key: string
  payload: Canceler
}


export const useCancelTokenStore = defineStore('cancelToken', () => {
  const httpRequestMap = new Map<string, Canceler>()

  const addHttpRequestMap = (payload?: ReqObj) => {
    if (!payload) {
      for (const [key, val] of httpRequestMap) {
        val('interrupt')
      }
      httpRequestMap.clear()
    } else {
      if (httpRequestMap.has(payload.key)) {
        (httpRequestMap.get(payload.key) as Canceler)('interrupt')
        httpRequestMap.delete(payload.key)
      }
      httpRequestMap.set(payload.key, payload.payload)
    }
  }

  const removeHttpRequestMap = async (key?: string) => {
    if (key) {
      if (httpRequestMap.has(key)) {
        (httpRequestMap.get(key) as Canceler)('interrupt')
        httpRequestMap.delete(key)
      }
    } else {
      addHttpRequestMap()
    }
  }

  return {
    httpRequestMap,
    addHttpRequestMap,
    removeHttpRequestMap
  }
})
