<!-- 创建项目 -->
<template>
  <a-form :model="formState" ref="formRef" name="basic" :label-col="{ style: { width: '100px' } }" autocomplete="off"
    @finish="onFinish">
    <a-form-item label="项目名" name="appName" :rules="[{ required: true, message: '请输入项目名' }]">
      <a-input v-model:value="formState.appName" :maxlength="64" placeholder="请输入项目名" />
    </a-form-item>
    <a-form-item label="负责人" name="projectManagers" :rules="[{ required: true, message: '请输入负责人' }]">
      <ZSelect :showSearch="true" :find-url="'/ioa/api/sys/user/findName'" subtitleKey="name" searchKey="keywords"
        bingValue="username" mode="multiple" bingLabel="username" v-model:value="formState.projectManagers"
        placeholder="请选择用户" :multipleLabel="true" bingMultipleLabel="name">
      </ZSelect>
    </a-form-item>
    <a-form-item label="部门">
      {{ formState.orgName }}
    </a-form-item>
    <a-form-item label="描述" name="description" :rules="[{ required: false, message: '描述' }]">
      <a-input v-model:value="formState.description" :maxlength="200" placeholder="描述" />
    </a-form-item>
  </a-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { queryOrgNameAPI } from '@/api/system/org-service';
import { apiSave } from '@/api/project-service'
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
  description: ''
});

if (appStore.userInfo) {
  formState.orgName = appStore.userInfo.orgName || ''
  formState.projectManagers = [appStore.userInfo.username]
}

const formRef = ref()

const queryOrgName = () => {
  if (appStore.userInfo?.username) {
    queryOrgNameAPI(appStore.userInfo.username).then(res => {
      if (res.success) {
        formState.orgName = res.data.orgName
      }
    })
  }
}
queryOrgName()

/** 保存/发布 ============================================= */
const onFinish = () => {
  formRef.value.validate().then(() => {
    console.log(11);
    let data = {
      ...formState,
      projectManagers: (formState.projectManagers as Array<string>)?.join(';')
    }
    console.log(data, 'data');
    doSave(data)
  })
};
defineExpose({
  onFinish
})

const doSave = (data: any) => {
  apiSave(data).then(res => {
    if (res.success) {
      message.success('新增成功')
      Object.assign(formState, {
        appName: '',
        description: ''
      })
      formRef.value.resetFields()
      emit('close', {
        ...data,
      })
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
