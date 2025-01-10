<docs>
---
order: 5
title: 额外标题 多选
---

## zh-CN
multipleLabel 属性控制是否展示额外标题，bingMultipleLabel 属性指定绑定的字段名。

selectRecord 方法返回选中的对象数据。

changeRecord 方法返回选中的所有数据对象集合，支持数据初始化时触发该方法。

change 方法返回选中的所有数据集合。

</docs>

<template>
  <ZSelect :find-url="'/system/sys/role/find'" mode="multiple" v-model:value="value" @selectRecord="selectRecord"
    @changeRecord="changeRecord" @change="change" placeholder="请选择数据" :multipleLabel="true" bingMultipleLabel="codes">
  </ZSelect>
</template>
<script lang="ts" setup>
import { ref, watch } from 'vue'
import { ZSelect } from 'zui-v3'
const value = ref(undefined)
watch(() => value.value, (val) => {
  console.log('val', val);
})
function change(record, option) {
  console.log('change', record);
  console.log('option', option);
}
function selectRecord(record) {
  console.log('selectRecord', record);
}
function changeRecord(record) {
  console.log('changeRecord', record);
}
</script>
