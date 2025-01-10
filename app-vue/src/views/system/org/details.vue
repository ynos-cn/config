<!-- 机构-详情 -->
<template>
  <Descriptions :title="pFormData.name">
    <DescriptionsItem label="名称">{{ pFormData.name }}</DescriptionsItem>
    <DescriptionsItem label="机构代码">{{ pFormData.code }}</DescriptionsItem>
    <DescriptionsItem label="创建时间">{{ dayjs(pFormData.createTime).format("YYYY-MM-DD HH:mm:ss") }}</DescriptionsItem>
    <DescriptionsItem label="负责人名称">{{ pFormData.controllerName }}</DescriptionsItem>
    <DescriptionsItem label="负责人联系电话">{{ pFormData.controllerTel }}</DescriptionsItem>
    <DescriptionsItem label="所属机构">{{ pFormData.orgName }}</DescriptionsItem>
  </Descriptions>
</template>

<script lang="ts" setup>
import { OrgStruct } from '@/interface/org';
import { Descriptions, DescriptionsItem } from 'ant-design-vue'
import { PropType } from 'vue';
import dayjs from 'dayjs';

defineProps({
  pFormData: {
    type: Object as PropType<OrgStruct>,
    default: {}
  },
})
</script>
<style lang='less' scoped></style>
