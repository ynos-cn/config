<!-- 创建角色 -->
<template>
  <a-form :model="formState" ref="formRef" name="basic" :label-col="{ style: { width: '100px' } }" autocomplete="off"
    @finish="onFinish">
    <a-form-item label="角色名" name="name" :rules="[{ required: true, message: '请输入角色名' }]">
      <a-input v-model:value="formState.name" :maxlength="32" placeholder="请输入角色名" />
    </a-form-item>
    <a-form-item label="人员列表" name="person" :rules="[{ required: true, message: '请选择人员' }]">
      <a-input v-show="false" v-model:value="formState.person" :maxlength="32" placeholder="请输入角色名" />
      <a-form-item-rest>
        <div class="tag" :style="{ marginTop: showUserModal ? '5px' : 0 }">
          <span v-if="persons.length <= 0">请选择用户</span>
          <a-tag v-for="item in persons" :key="item.names" :closable="true" @close="onClose(item.names)">
            {{ item.names }}
          </a-tag>
          <PlusCircleOutlined style="margin-left: 5px;" v-if="!showUserModal" @click="onAddUser" />
        </div>
        <a-input-group v-if="showUserModal" compact style="margin-top: 10px;">
          <a-select v-model:value="userType">
            <a-select-option :value="1">OA用户</a-select-option>
            <a-select-option :value="2">OA组织</a-select-option>
          </a-select>
          <ZSelect v-if="userType == 1" style="width: 400px;" :showSearch="true"
            :find-url="'/ioa/api/sys/user/findName'" subtitleKey="name" searchKey="keywords" bingValue="username"
            bingLabel="username" placeholder="请选择用户" :multipleLabel="true" v-model:value="userValue"
            bingMultipleLabel="name" @change-record="onUserChange">
          </ZSelect>
          <OrgTreeSelect v-if="userType == 2" :checkedKeys="orgValue" @check="onOrgCheck" style="width: 400px;"
            :allowClear="true" :checkable="true" :all="true">
          </OrgTreeSelect>
        </a-input-group>
      </a-form-item-rest>
    </a-form-item>
    <a-form-item label="分组" name="object" :rules="[{ required: true, message: '请输入分组' }]">
      <a-input v-model:value="formState.object" placeholder="请输入分组" />
      <p class="desc-text">
        “分组”可指定为分组或分组的前缀，例如：分组为 DEV 的权限，对分组名 DEV.xxx 和 Devyy 都生效。特别的，* 表示匹配所有分组。用英文分号(;)分隔多个分组，如：DEV;TEST
      </p>
    </a-form-item>
    <a-form-item label="权限" name="permissionTypes">
      <a-radio-group v-model:value="permission">
        <a-radio :style="radioStyle" :value="1">只读配置
          <span style="padding-left: 20px;" class="desc-text">分组只读权限</span>
        </a-radio>
        <a-radio :style="radioStyle" :value="2">读写和发布配置
          <span style="padding-left: 20px;" class="desc-text">包含读配置的权限</span>
          <div class="permission" v-if="permission == 2">
            <a-checkbox-group @change="onCheckbox" v-model:value="permissions"
              :options="PermissionType.filter(e => e.type == 2)" />
          </div>
        </a-radio>
        <a-radio :style="{ ...radioStyle, marginTop: permission == 2 ? '32px' : 0 }" :value="6">管理分组
          <span style="padding-left: 20px;" class="desc-text">分组的所有权限，包含读写和发布的所有权限点，包含修改分组的高级功能</span>
        </a-radio>
      </a-radio-group>
    </a-form-item>
  </a-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { apiSave } from '@/api/role-service'
import { ZSelect, OrgTreeSelect } from '@/components';
import { message } from 'ant-design-vue'
import { PlusCircleOutlined } from '@ant-design/icons-vue'
import { Person, RoleStruct } from '@/interface';
import { useAppStore } from '@/store/app'
import { PermissionType } from './setting'
import { useRoute } from 'vue-router'

const route = useRoute()
const emit = defineEmits(['close'])
const appStore = useAppStore()

const formState = reactive<RoleStruct>({
  name: '',
  permissionTypes: [],
  person: '',
});

/** ====================== 权限 ==================== */
const permission = ref(1)
const permissions = ref([2, 3, 4, 8, 11, 10])
const radioStyle = reactive({
  display: 'flex',
  height: '30px',
  lineHeight: '30px',
});
let oldArr: Array<number> = []
const onCheckbox = (e) => {
  if (e.length < 1) {
    message.warning('至少需要选择一个权限');
    permissions.value = oldArr
    return
  }
  oldArr = permissions.value
}
/** ====================== 权限 ==================== */

const formRef = ref()

/** ====================== 添加用户 ====================== */
const showUserModal = ref(false)
const userType = ref(1)
const userValue = ref()
const orgValue = ref([])
const persons = ref<Array<Person>>([])
const onAddUser = () => {
  showUserModal.value = true
}
const onUserChange = (user) => {
  if (user.username) {
    if (!persons.value.some(e => e.names == user.username)) {
      persons.value.push({
        names: user.username,
        type: 1
      })
      formState.person = persons.value.map(e => e.names).join(';')
    }
  }
  setTimeout(() => {
    userValue.value = undefined
    formRef.value.validateFields(["person"])
  }, 100)
}
const onOrgCheck = (org) => {
  if (org) {
    let index = persons.value.findIndex(e => e.names == org.fullName)
    if (index > 0) {
      persons.value.splice(index, 1)
    } else {
      persons.value.push({
        names: org.fullName,
        type: 2,
        orgIds: org.id
      })
    }
    formState.person = persons.value.map(e => e.names).join(';')
  }
  setTimeout(() => {
    formRef.value.validateFields(["person"])
  }, 100)
}
const onClose = (names) => {
  if (names) {
    persons.value = persons.value.filter(e => e.names != names)
    formState.person = persons.value.map(e => e.names).join(';')
  }
}
/** ====================== 添加用户 ====================== */

/** ============= 保存/发布 ============= */
const onFinish = () => {
  formRef.value.validate().then(() => {
    let permissionTypes: Array<number> = []
    if ([1, 6].includes(permission.value)) {
      permissionTypes = [permission.value]
    } else {
      permissionTypes = permissions.value
    }

    let _persons: Array<Person> = []
    Array.from(new Set(persons.value.map(e => e.type))).map(v => {
      console.log(v, '类型');
      _persons.push({
        type: v,
        names: persons.value.filter(e => e.type == v).map(e => e.names).join(';'),
        orgIds: v == 2 ? persons.value.filter(e => e.type == v).map(e => e.orgIds).join(';') : undefined,
      })
    })

    let data = {
      appId: route.params.id,
      name: formState.name,
      object: formState.object,
      envNames: ["Defalut"],
      permissionTypes,
      persons: _persons
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
      emit('close', {
        ...data,
      })
    } else {
      message.error(res.msg)
    }
  }).catch(err => {
    console.error(err)
  })
}
/** 保存/发布 ============================================= */

</script>
<style lang='less' scoped>
.desc-text {
  opacity: .4;
  font-family: Helvetica;
  font-size: 12px;
  color: #000;
  clear: both;
  line-height: 24px;
}
</style>
