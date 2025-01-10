/*
 * @Description: 脚本
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2024-01-15 17:52:43
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2024-01-15 17:53:09
 */
import { ipcMain, app } from 'electron'

ipcMain.on('close', (e) => {
  app.exit(0);
})
