<!--
 * @Description: 动态渲染组件
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2022-08-08 15:32:21
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2022-08-08 15:58:50
-->
<!-- 动态渲染组件 -->
<template>
  <component :is="component" v-bind="attrs"></component>
</template>

<script lang="ts" setup>
defineProps({
  component: {
    type: String,
  },
  attrs: {
    type: Object,
    default: () => { }
  }
})

</script>
<style lang='less' scoped>
</style>