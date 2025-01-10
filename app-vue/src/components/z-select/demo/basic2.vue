<!--
 * @Description: 
 * @Version: 2.0
 * @Autor: xuhan
 * @Date: 2022-09-15 20:21:18
 * @LastEditors: xuhan
 * @LastEditTime: 2022-09-15 20:48:45
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
  <ZSelect :find-url="'/system/sys/role/find'" v-model:value="value" mode="tags" :max-tagCount="2">
  </ZSelect>
</template>
<script lang="ts" setup>
import { ref, watch } from 'vue'
import { ZSelect } from 'zui-v3'
const value = ref('')
const sid = ref('')
watch(() => value.value, (val: any) => {
  console.log(val);
})
</script>