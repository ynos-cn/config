<!--
 * @Description: 404
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-08-24 11:30:07
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2022-08-24 16:09:29
-->
<template>
  <Result status="404" title="404" style="background: none" sub-title="抱歉，您访问的页面不存在。">
    <template #extra>
      <router-link to="/">
        <Button type="primary">返回首页</Button>
      </router-link>
    </template>
  </Result>
  <!-- <div class="exception">
  </div> -->
</template>

<script lang="ts" setup>
import { Result, Button } from 'ant-design-vue'
</script>
<style lang="less" scoped>
.exception {
  width: 100%;
  height: 100%;
  background-image: url("@/assets/base/404页面.png");
  background-repeat: no-repeat;
  background-size: 100% 100%;
}
</style>