const fs = require("fs");
const path = require("path");
const execSync = require("child_process").execSync;
const os = require("os");

const { version } = require("../package.json");

// @ts-ignore
Date.prototype.Format = function (fmt) {
  //author: meizz
  var o = {
    "M+": this.getMonth() + 1, //月份
    "d+": this.getDate(), //日
    "h+": this.getHours(), //小时
    "m+": this.getMinutes(), //分
    "s+": this.getSeconds(), //秒
    S: this.getMilliseconds(), //毫秒
  };
  if (/(y+)/.test(fmt))
    fmt = fmt.replace(
      RegExp.$1,
      (this.getFullYear() + "").substr(4 - RegExp.$1.length)
    );
  for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt))
      fmt = fmt.replace(
        RegExp.$1,
        RegExp.$1.length == 1 ? o[k] : ("00" + o[k]).substr(("" + o[k]).length)
      );
  return fmt;
};

/** 当前时间 */
// @ts-ignore
const currentTime = new Date().Format("yyyy-MM-dd hh:mm:ss");
/** 当前git版本号 */
const gitCommitId = execSync("git show -s --format=%H")?.toString()?.trim();

const url = path.join(
  __dirname,
  "..",
  "src",
  "components",
  "version",
  "version.ts"
);

//获取本机ip
function getIpAddress() {
  /**os.networkInterfaces() 返回一个对象，该对象包含已分配了网络地址的网络接口 */
  var interfaces = os.networkInterfaces();
  for (var devName in interfaces) {
    var iface = interfaces[devName];
    // @ts-ignore
    for (var i = 0; i < iface.length; i++) {
      // @ts-ignore
      var alias = iface[i];
      if (
        alias.family === "IPv4" &&
        alias.address !== "127.0.0.1" &&
        !alias.internal
      ) {
        return alias.address;
      }
    }
  }
}

const fileExists = fs.existsSync(url);

if (fileExists) {
  fs.unlinkSync(url);
} else {
  let mkdirStr = "";
  if (os.type() == "Windows_NT") {
    //windows平台
    mkdirStr = url.split("\\version.ts")[0];
  }
  if (os.type() == "Darwin" || os.type() == "Linux") {
    mkdirStr = url.split("/version.ts")[0];
  }
  fs.mkdirSync(mkdirStr);
}

/** 版本号 */
const versionNumber = `/** 版本号 */\nexport const version = \"${version}\";`;
/** 当前时间 */
const currentTimeStr = `/** 当前时间 */\nexport const currentTime = \"${currentTime}\";`;
/** 构建ip */
const buildIp = `/** 构建ip */\nexport const buildIp = \"${getIpAddress()}\";`;
/** 当前git提交号 */
const commitId = `/** 当前git提交号 */\nexport const gitCommitId = \"${gitCommitId}\";\n`;

const fileContent = `${versionNumber}\n${currentTimeStr}\n${buildIp}\n${commitId}`;
fs.writeFileSync(url, fileContent, "utf8");

// 程序执行结束
console.info("\x1B[32m%s\x1b[0m", "【version】信息处理完成！");
