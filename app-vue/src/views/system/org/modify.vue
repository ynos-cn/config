<!-- 机构管理 -->
<template>
  <div class="modify">
    <a-form :model="formState" name="basic" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }" autocomplete="off"
      @finish="onFinish">
      <a-form-item label="名称" name="name" :rules="[{ required: true, message: '请输入机构名称' }]">
        <a-input v-model:value="formState.name" :maxlength="50" placeholder="请输入机构名称" />
      </a-form-item>
      <a-form-item label="机构代码" name="code" :rules="[{ required: false, message: '请输入机构代码' }]">
        <a-input v-model:value="formState.code" :maxlength="20" placeholder="请输入机构代码" />
      </a-form-item>
      <a-form-item label="负责人姓名" name="controllerName" :rules="[{ required: false, message: '请输入负责人姓名' }]">
        <a-input v-model:value="formState.controllerName" :maxlength="20" placeholder="请输入负责人姓名" />
      </a-form-item>
      <a-form-item label="负责人联系电话" name="controllerTel" :rules="[{ required: false, message: '请输入负责人联系电话' }]">
        <a-input v-model:value="formState.controllerTel" :maxlength="20" placeholder="请输入负责人联系电话" />
      </a-form-item>
      <div class="footer">
        <a-button class="btn" type="primary" html-type="submit" :disabled="editType == OperateCMD.details">保存</a-button>
      </div>
    </a-form>
  </div>
</template>

<script lang="ts" setup>
import { reactive, PropType, watch, ref } from 'vue'
import { apiSave } from '@/api/system/org-service';
import { message } from 'ant-design-vue'
import { OperateCMD } from '@/hooks/useManage';
import { OrgStruct } from '@/interface/org';
import { BaseParams } from '@/interface/base';
import { apiFind } from '@/api/system/org-service'
import { useAppStore } from '@/store/app'
import { clearFormState } from '@/utils/utils';

const emit = defineEmits(['close'])
const appStore = useAppStore()

const props = defineProps({
  pFormData: {
    type: Object as PropType<OrgStruct>,
    default: undefined
  },
  editType: {
    type: Number as PropType<OperateCMD>,
    default: OperateCMD.details
  },
  options: {
    type: Array as PropType<Array<OrgStruct>>,
    default: []
  }
})

const formState = reactive<OrgStruct>({
  name: '',
  code: '',
  controllerName: '',
  controllerTel: ''
});

/** 保存/发布 ============================================= */
const onFinish = (values: any) => {
  let data = {
    id: props.editType === OperateCMD.new ? undefined : props.pFormData?.id,
    ...values,
    orgId: props.pFormData?.orgId,
    orgName: props.pFormData?.orgName
  }
  doSave(data)
};
const doSave = (data: any) => {
  apiSave(data).then(res => {
    if (res.success) {
      message.success(props.editType === 1 ? '新增成功' : '修改成功')
      emit('close', {
        ...props.pFormData,
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

watch(() => props.pFormData, (val) => {
  if (val) {
    Object.assign(formState, {
      ...val,
    })
  } else {
    clearFormState(formState)
  }
}, { immediate: true, deep: true })


/** 取消 ============================================== */
const onCancel = () => {
  emit('close')
}
/** 取消 ============================================== */

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
