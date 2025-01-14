<!-- 创建项目 -->
<template>
  <a-form :model="formState" ref="formRef" name="basic" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }"
    autocomplete="off" @finish="onFinish">
    <a-form-item label="项目名" name="name" :rules="[{ required: true, message: '请输入项目名' }]">
      <a-input v-model:value="formState.name" :maxlength="50" placeholder="请输入项目名" />
    </a-form-item>
    <a-form-item label="负责人" name="code" :rules="[{ required: true, message: '请输入负责人' }]">
      <a-input v-model:value="formState.code" :maxlength="20" placeholder="请输入负责人" />
    </a-form-item>
    <a-form-item label="部门" name="controllerName" :rules="[{ required: true, message: '请输入部门' }]">
      <a-input v-model:value="formState.controllerName" :maxlength="20" placeholder="请输入部门" />
    </a-form-item>
    <a-form-item label="描述" name="controllerTel" :rules="[{ required: false, message: '请输入描述' }]">
      <a-input v-model:value="formState.controllerTel" :maxlength="20" placeholder="请输入描述" />
    </a-form-item>
  </a-form>
</template>

<script lang="ts" setup>
import { reactive, PropType, watch, ref } from 'vue'
import { apiSave } from '@/api/system/org-service';
import { message } from 'ant-design-vue'
import { OrgStruct } from '@/interface/org';
import { useAppStore } from '@/store/app'

const emit = defineEmits(['close'])
const appStore = useAppStore()

const formState = reactive<OrgStruct>({
  name: '',
  code: '',
  controllerName: '',
  controllerTel: ''
});

const formRef = ref()

/** 保存/发布 ============================================= */
const onFinish = (values: any) => {
  formRef.value.validate().then(() => {
    console.log(11);
    let data = {
      ...values,
    }
    console.log(data, 'data');
  })
  // doSave(data)
};

defineExpose({
  onFinish
})

const doSave = (data: any) => {
  apiSave(data).then(res => {
    if (res.success) {
      message.success('新增成功')
    } else {
      message.error(res.msg)
    }
  }).catch(err => {
    if (err?.response?.data?.msg) {
      message.error(err?.response?.data?.msg)
    }
  })
}
/** 保存/发布 ============================================= */

</script>
<style lang='less' scoped>
.footer {
  width: 100%;
  text-align: center;

  .btn {
    margin-right: 5px;

    &:last-child {
      margin-right: 0;
    }
  }
}
</style>
