<!-- 创建项目 -->
<template>
  <a-form :model="formState" ref="formRef" name="basic" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }"
    autocomplete="off" @finish="onFinish">
    <a-form-item label="项目名" name="appName" :rules="[{ required: true, message: '请输入项目名' }]">
      <a-input v-model:value="formState.appName" :maxlength="50" placeholder="请输入项目名" />
    </a-form-item>
    <a-form-item label="负责人" name="projectManagers" :rules="[{ required: true, message: '请输入负责人' }]">
      <ZSelect :find-url="'/ioa/api/sys/user/find'" bingValue="username" bingLabel="username" mode="multiple"
        v-model:value="formState.projectManagers" placeholder="请选择用户" :multipleLabel="true" bingMultipleLabel="codes">
      </ZSelect>
    </a-form-item>
    <a-form-item label="部门">
      {{ formState.orgName }}
    </a-form-item>
    <a-form-item label="描述" name="description" :rules="[{ required: false, message: '请输入描述' }]">
      <a-input v-model:value="formState.description" :maxlength="20" placeholder="请输入描述" />
    </a-form-item>
  </a-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { apiSave } from '@/api/system/org-service';
import { message } from 'ant-design-vue'
import { ProjectStruct } from '@/interface/Project';
import { useAppStore } from '@/store/app'
import ZSelect from '@/components/z-select'

const emit = defineEmits(['close'])
const appStore = useAppStore()

const formState = reactive<ProjectStruct>({
  appName: '',
  projectManagers: [],
  pullSwitch: 0,
  envSwitch: 0,
  orgName: '',
  description: ' '
});

if (appStore.userInfo) {
  formState.orgName = appStore.userInfo.orgName || ''
  formState.projectManagers = [appStore.userInfo.username]
}

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
