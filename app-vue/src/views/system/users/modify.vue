<!-- 用户管理 -->
<template>
  <div class="modify">
    <a-form :model="formState" name="basic" :label-col="{ span: 6 }" :wrapper-col="{ span: 16 }" autocomplete="off"
      @finish="onFinish">
      <a-form-item label="姓名" name="name" :rules="[{ required: true, message: '请输入姓名' }]">
        <a-input v-model:value="formState.name" :maxlength="50" placeholder="请输入姓名" />
      </a-form-item>
      <a-form-item label="手机号码" name="phone" :rules="[{ required: true, message: '请输入手机号码' }]">
        <a-input v-model:value="formState.phone" :maxlength="20" placeholder="请输入手机号码" />
      </a-form-item>
      <a-form-item label="职位" name="position" :rules="[{ required: false, message: '请输入职位' }]">
        <a-input v-model:value="formState.position" :maxlength="200" placeholder="请输入职位" />
      </a-form-item>
      <a-form-item label="入职时间" name="joinTime" :rules="[{ required: true, message: '请填写入职时间' }]">
        <a-date-picker v-model:value="formState.joinTime" placeholder="请选择入职时间" />
      </a-form-item>
      <a-form-item label=" 性别" name="sex" :rules="[{ required: false, message: '请选择性别' }]">
        <a-select :options="sexOptions" v-model:value="formState.sex" placeholder="请选择性别"> </a-select>
      </a-form-item>
      <a-form-item label="邮箱" name="email" :rules="[{ required: false, message: '请输入邮箱' }]">
        <a-input v-model:value="formState.email" :maxlength="200" placeholder="请输入邮箱" />
      </a-form-item>
      <a-form-item label="所属机构" name="orgId" :rules="[{ required: true, message: '请选择所属机构' }]">
        <OrgTreeSelect v-model:value="formState.orgId" @select="onOrgSelect" />
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
import { apiSave } from '@/api/system/user-service';
import { message } from 'ant-design-vue'
import { OperateCMD } from '@/hooks/useManage';
import { UserStruct } from '@/interface/user';
import dayjs from 'dayjs';
import { useAppStore } from '@/store/app'
import OrgTreeSelect from '@/components/orgTreeSelect/index.vue'

const emit = defineEmits(['close'])
const appStore = useAppStore()

const props = defineProps({
  pFormData: {
    type: Object as PropType<UserStruct>,
    default: {}
  },
  editType: {
    type: Number as PropType<OperateCMD>,
    default: 2
  },
  options: {
    type: Array as PropType<Array<UserStruct>>,
    default: []
  }
})

const formState = reactive<UserStruct>({
  name: '',
  phone: '',
  status: 1,
  sex: 1,
  joinTime: dayjs(),
});


const sexOptions = [
  { label: '男', value: 1 },
  { label: '女', value: 0 }
]

/** 获取所属机构 =========================================== */
let orgName = ''
const onOrgSelect = (value) => {
  orgName = value.name
}
/** 获取所属机构 =========================================== */

/** 保存/发布 ============================================= */
const onFinish = (values: any) => {
  let data = {
    id: props.editType === 1 ? undefined : props.pFormData.id,
    ...values,
    orgName,
    joinTime: values.joinTime ? dayjs(values.joinTime).format("YYYY-MM-DD HH:mm:ss") : undefined
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
      joinTime: val.joinTime ? dayjs(val.joinTime) : dayjs(),
    })
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
