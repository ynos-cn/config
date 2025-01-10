<docs>
---
order: 0
title: 基本使用
---

## zh-CN

基本使用。

</docs>

<template>
  <ZSelect :find-url="'/system/sys/role/find'" v-model:value="value">
  </ZSelect>
</template>
<script lang="ts" setup>
import { ref, watch } from 'vue'
import { ZSelect } from 'zui-v3'
const value = ref('')
watch(() => value.value, (val) => {
  console.log(val);
})
</script>
