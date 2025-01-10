/*
 * @Description: 客户端入口
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2024-01-15 11:19:42
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2024-01-15 17:53:23
 */
import { app, BrowserWindow, Menu, dialog, ipcMain } from 'electron'
import path from 'path'
import "./script"

// 是否是生产环境
const isPackaged = app.isPackaged;

// 禁止显示默认菜单
Menu.setApplicationMenu(null);

// 主窗口
var mainWindow;

const createWindow = () => {
  mainWindow = new BrowserWindow({
    // 默认窗口标题，如果由loadURL()加载的HTML文件中含有标签<title>，此属性将被忽略。
    title: "app",
    width: 1920,
    height: 1080,
    webPreferences: {
      contextIsolation: false, // 是否开启隔离上下文
      nodeIntegration: true, // 渲染进程使用Node API
      preload: path.join(__dirname, "preload.js"), // 在页面运行其他脚本之前预先加载指定的脚本
    },
    visualEffectState: "active", // 窗口的可视化状态
    // 设置窗口尺寸为屏幕工作区尺寸
    // width: screen.getPrimaryDisplay().workAreaSize.width,
    // height: screen.getPrimaryDisplay().workAreaSize.height,
    // 窗口图标。 在 Windows 上推荐使用 ICO 图标来获得最佳的视觉效果, 默认使用可执行文件的图标.
    // 在根目录中新建 build 文件夹存放图标等文件
    icon: path.resolve(__dirname, "./favicon.png"),
  })

  // 加载文件
  function load() {
    mainWindow.loadURL(
      isPackaged
        ? `file://${path.join(__dirname, "./index.html")}`
        : "http://localhost:8888"
    );
  }

  // 开发环境下，打开开发者工具。
  if (!isPackaged) {
    // 生产环境下，load 的是 html 文件，要做特殊处理。
    // 加载失败之后触发
    mainWindow.webContents.on("did-fail-load", () => {
      load();
    });

    // // 当用户或页面想要导航时触发。
    // // 它可能发生在 window.location 对象改变或用户点击页面上的链接时，可能会发生这种情况。
    // // 当使用如 webContents.loadURL 和 webContents.back APIs 以编程方式导航时，将不会触发此事件。
    // // 页面内导航也不会触发，例如点击锚点或更新 window.location.hash。 可使用 did-navigate-in-page 事件。
    // mainWindow.webContents.on("will-navigate", (event, url) => {
    //   event.preventDefault();
    //   load();
    // });

    // // 禁止使用快捷键刷新
    // mainWindow.webContents.on("before-input-event", (event, input) => {
    //   mainWindow.webContents.setIgnoreMenuShortcuts(
    //     input.key.toLowerCase() === "f5" ||
    //     (input.control && input.key.toLowerCase() === "r") ||
    //     (input.meta && input.key.toLowerCase() === "r")
    //   );
    // });

    mainWindow.webContents.openDevTools();
  }

  // 在窗口要关闭的时候触发
  mainWindow.on("close", (e) => {
    e.preventDefault();
    dialog
      .showMessageBox(mainWindow, {
        type: "info",
        title: "退出提示",
        defaultId: 0,
        cancelId: 1,
        message: "确定要退出吗？",
        buttons: ["退出", "取消"],
      })
      .then((res) => {
        if (res.response === 0) {
          app.exit(0);
        }
      });
  });

  load()
}
process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true'

// 在应用准备就绪时调用函数
app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    // 通常在 macOS 上，当点击 dock 中的应用程序图标时，如果没有其他
    // 打开的窗口，那么程序会重新创建一个窗口。
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
})

ipcMain.on('max', () => {
  if (mainWindow.isMaximized()) {  //判断窗口是否最大化
    mainWindow.restore()    //将窗口恢复为之前的状态
  } else {
    mainWindow.maximize()   //将窗口全屏
  }
})

// 除了 macOS 外，当所有窗口都被关闭的时候退出程序。 因此，通常对程序和它们在任务栏上的图标来说，应当保持活跃状态，直到用户使用 Cmd + Q 退出。
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

// 如果开发环境使用了 nginx 代理，禁止证书报错
if (!isPackaged) {
  // 证书的链接验证失败时，触发该事件
  app.on(
    "certificate-error",
    function (event, webContents, url, error, certificate, callback) {
      event.preventDefault();
      callback(true);
    }
  );
}