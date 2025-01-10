<!--
 * @Description: 
 * @Version: 2.0
 * @Autor: xuhan
 * @Date: 2022-09-15 20:21:18
 * @LastEditors: xuhan
 * @LastEditTime: 2022-09-15 20:59:36
-->
<docs>
---
order: 0
title: 基本使用
---

## zh-CN

基本使用。

</docs>

<template>
  <!-- <div v-for="item in size">

  </div> -->
  <ZSelect :find-url="'event/api/waterLevel/findGroupByRiverStation'" v-model:value="value" mode="tags" :max-tag-text-length="4" :show-arrow="true">
  </ZSelect>
  <ZSelect :find-url="'event/api/waterLevel/findGroupByRiverStation'" v-model:value="value" mode="tags" :max-tag-text-length="4" :show-arrow="true">
  </ZSelect>
</template>
<script lang="ts" setup>
import { ref, watch } from 'vue'
import { ZSelect } from 'zui-v3'
const value = ref('')
// const size = [
//   {value: 'small'}
// ]
watch(() => value.value, (val: any) => {
  console.log(val);
})
</script>