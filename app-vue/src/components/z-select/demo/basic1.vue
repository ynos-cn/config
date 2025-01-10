<!--
 * @Description: 
 * @Version: 2.0
 * @Autor: xuhan
 * @Date: 2022-09-15 17:49:39
 * @LastEditors: xuhan
 * @LastEditTime: 2022-09-15 20:50:54
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
  <ZSelect class="width1" :find-url="'/system/sys/role/find'" :param-body-data="{sid: '2717231246162362450'}" v-model:value="value">
  </ZSelect>
  <ZSelect class="width1" :find-url="'/system/sys/role/find'" :param-body-data="{sid: '2717231246162362450'}" v-model:value="value" :disabled="true">
  </ZSelect>
  <ZSelect class="width1" :find-url="'/system/sys/role/find'" :param-body-data="{sid: '2717231246162362450'}" v-model:value="value" :dropdown-style="{backgroundColor:'red'}">
  </ZSelect>
</template>
<script lang="ts" setup>
import { ref, watch } from 'vue';
import { ZSelect } from 'zui-v3';
const value = ref('');
const pushData = [
  {codes: "11", created: "2021-05-21 15:28:26",createdBy: "2659837563826167862",descs: "1111111111",ids: null,keywords: null,lastUpdated: "2021-05-2115:28:26",lastUpdatedBy: "2659837563826167862",name: "111",orgId: "2659837563826167861",sid: "2712661933535363091",tenantId: "50",types: null,userId: null}
]
watch(() => value.value, (val) => {
  console.log(val);
});
</script>
<style>
  .width1 {
    width: 33.3%;
    padding: 0 2px;
  }
</style>