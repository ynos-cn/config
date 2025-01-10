<!-- 用户-详情 -->
<template>
  <Descriptions :title="pFormData.name">
    <DescriptionsItem label="姓名">{{ pFormData.name }}</DescriptionsItem>
    <DescriptionsItem label="手机号码">{{ pFormData.phone }}</DescriptionsItem>
    <DescriptionsItem label="入职时间">{{ pFormData.joinTime }}</DescriptionsItem>
    <DescriptionsItem label="职位">{{ pFormData.position }}</DescriptionsItem>
    <DescriptionsItem label="性别">
      {{ pFormData.sex == undefined ? '未知' : pFormData.sex == 1 ? '男' : '女' }}
    </DescriptionsItem>
    <DescriptionsItem label="邮箱">{{ pFormData.email }}</DescriptionsItem>
    <DescriptionsItem label="所属机构">{{ pFormData.orgName }}</DescriptionsItem>
    <DescriptionsItem label="状态">{{ pFormData.status == 1 ? '可用' : '禁用' }}</DescriptionsItem>
    <DescriptionsItem label="创建时间">{{ dayjs(pFormData.createTime).format("YYYY-MM-DD HH:mm:ss") }}</DescriptionsItem>
  </Descriptions>
</template>

<script lang="ts" setup>
import { UserStruct } from '@/interface/user';
import { Descriptions, DescriptionsItem } from 'ant-design-vue'
import { PropType } from 'vue';
import dayjs from 'dayjs';

defineProps({
  pFormData: {
    type: Object as PropType<UserStruct>,
    default: {}
  },
})
</script>
<style lang='less' scoped></style>
