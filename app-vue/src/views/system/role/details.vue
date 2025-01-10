<!-- 角色-详情 -->
<template>
  <Descriptions :title="pFormData.name">
    <DescriptionsItem label="名称">{{ pFormData.name }}</DescriptionsItem>
    <DescriptionsItem label="角色代码">{{ pFormData.code }}</DescriptionsItem>
    <DescriptionsItem label="创建时间">{{ dayjs(pFormData.createTime).format("YYYY-MM-DD HH:mm:ss") }}</DescriptionsItem>
    <DescriptionsItem label="负责人名称">{{ pFormData.describe }}</DescriptionsItem>
  </Descriptions>
</template>

<script lang="ts" setup>
import { RoleStruct } from '@/interface/role';
import { Descriptions, DescriptionsItem } from 'ant-design-vue'
import { PropType } from 'vue';
import dayjs from 'dayjs';

defineProps({
  pFormData: {
    type: Object as PropType<RoleStruct>,
    default: {}
  },
})
</script>
<style lang='less' scoped></style>
