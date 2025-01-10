<!--
 * @Description: 应用页面入口
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-07-26 14:04:04
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2022-10-25 11:58:52
-->
<!-- 应用页面入口 -->
<template>
  <ConfigProvider :locale="zh_CN" class="">
    <router-view />
  </ConfigProvider>
</template>

<script lang="ts" setup>
import { ConfigProvider } from 'ant-design-vue';
import zh_CN from 'ant-design-vue/es/locale/zh_CN';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';
dayjs.locale('zh-cn');
</script>
<style lang='less'>
@import url('@/components/global.less');

#app {
  width: 100%;
  height: 100%;
  overflow: auto;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  // -moz-user-select: none;
  // /*火狐*/
  // -webkit-user-select: none;
  // /*webkit浏览器*/
  // -ms-user-select: none;
  // /*IE10*/
  // -khtml-user-select: none;
  // /*早期浏览器*/
  // user-select: none;
  overflow: hidden;
}

.go-back {
  color: #02a7f0;
  font-size: 14px;
  cursor: pointer;
}

.ant-menu-root {
  background: #EBECF0;
}
</style>