<!-- 角色管理 -->
<template>
  <div class="modify">
    <a-form :model="formState" name="basic" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }" autocomplete="off"
      @finish="onFinish">
      <a-form-item label="名称" name="name" :rules="[{ required: true, message: '请输入角色名称' }]">
        <a-input v-model:value="formState.name" :maxlength="50" placeholder="请输入角色名称" />
      </a-form-item>
      <a-form-item label="角色代码" name="code" :rules="[{ required: false, message: '请输入角色代码' }]">
        <a-input v-model:value="formState.code" :maxlength="20" placeholder="请输入角色代码" />
      </a-form-item>
      <a-form-item label="描述" name="describe" :rules="[{ required: false, message: '请输入描述' }]">
        <a-textarea v-model:value="formState.describe" :maxlength="200" placeholder="请输入描述" />
      </a-form-item>
      <div class="footer">
        <a-button class="btn" type="primary" html-type="submit" v-if="editType != OperateCMD.details">保存</a-button>
        <a-button class="btn" @click="onCancel">取消</a-button>
      </div>
    </a-form>
  </div>
</template>

<script lang="ts" setup>
import { reactive, PropType, watch } from 'vue'
import { apiSave } from '@/api/system/role-service';
import { message } from 'ant-design-vue'
import { OperateCMD } from '@/hooks/useManage';
import { RoleStruct } from '@/interface/role';

const emit = defineEmits(['close'])

const props = defineProps({
  pFormData: {
    type: Object as PropType<RoleStruct>,
    default: {}
  },
  editType: {
    type: Number as PropType<OperateCMD>,
    default: 2
  },
  options: {
    type: Array as PropType<Array<RoleStruct>>,
    default: []
  }
})

const formState = reactive<RoleStruct>({
  name: '',
  code: '',
  describe: '',
});

/** 保存/发布 ============================================= */
const onFinish = (values: any) => {
  let data = {
    id: props.editType === 1 ? undefined : props.pFormData.id,
    ...values,
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
      ...val
    })
    if (props.editType === 1) {
      Object.assign(formState, {
        csName: ''
      })
    }
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
