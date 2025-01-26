<!-- 信息 -->
<template>
  <a-spin wrapperClassName="config-base" :spinning="loading">
    <a-card>
      <template #title>
        <div class="title">
          <span>基础信息</span>
          <span class="title-span">({{ formData?.creator }} 创建于 {{ formData?.createTime }})</span>
        </div>
      </template>
      <template #extra>
        <div class="extra">
          <span class="extra-span" v-show="command == OperateCMD.show" style="color: #0052d9;" @click="onEdit">编辑</span>
          <span class="extra-span" v-show="command == OperateCMD.show" style="color: #ff3e00;"
            @click="onDelete">删除项目</span>
          <span class="extra-span" v-show="command == OperateCMD.edit" style="color: #0052d9;" @click="onSave">保存</span>
          <span class="extra-span" v-show="command == OperateCMD.edit" style="color: #0052d9;"
            @click="command = OperateCMD.show">取消</span>
        </div>
      </template>
      <a-descriptions :column="2" class="config-base-des" :label-style="{ width: '110px', justifyContent: 'flex-end' }">
        <a-descriptions-item label="项目名" v-if="formData?.appName">
          <span v-if="command == OperateCMD.show">
            {{ formData.appName }}
          </span>
          <a-input v-else style="width: 80%;" :maxlength="64" v-model:value="formStore.appName" placeholder="请输入项目名" />
        </a-descriptions-item>
        <a-descriptions-item label="项目ID(Appid)">{{ formData?.appId }}</a-descriptions-item>
        <a-descriptions-item label="负责人" v-if="formData?.projectManagers">
          <span v-if="command == OperateCMD.show">
            {{ formData.projectManagers }}
            <a-tooltip>
              <template #title>负责人具有项目所有权限（如修改负责人列表、设置分角色权限等）</template>
              <span class="tip">
                <QuestionCircleOutlined />
              </span>
            </a-tooltip>
          </span>
          <ZSelect v-else style="width: 80%;" :showSearch="true" :find-url="'/ioa/api/sys/user/findName'"
            subtitleKey="name" searchKey="keywords" bingValue="username" mode="multiple" bingLabel="username"
            v-model:value="formStore.projectManagers" placeholder="请选择用户" :multipleLabel="true"
            bingMultipleLabel="name">
          </ZSelect>
        </a-descriptions-item>
        <a-descriptions-item label="部门">{{ formData?.orgName }}</a-descriptions-item>
        <a-descriptions-item label="描述" v-if="formData?.description">
          <span v-if="command == OperateCMD.show">
            {{ formData?.description }}
          </span>
          <a-textarea v-else style="width: 80%;" autoSize v-model:value="formStore.description" placeholder="描述"
            :maxlength="200" />
        </a-descriptions-item>
        <a-descriptions-item label="配置拉取签名" v-if="typeof formData?.pullSwitch != 'undefined'">
          <a-switch :checked="pullSwitch" checked-children="启用" un-checked-children="关" @change="onPullSwitch" />
          <a-tooltip>
            <template #title>
              <p> 配置拉取接口：可以启用签名来保障数据拉取的安全，不需要加入角色列表来授权。</p>
              <p> 配置管理接口：不受此开关控制；必须使用签名来保障数据不被意外修改，需加入角色列表来限制权限类型。</p>
              <p>获取 user_id 的办法：在页面下方添加自定义用户后，后台自动生成user_id和secret_key。</p>
            </template>
            <span class="tip">
              <QuestionCircleOutlined />
            </span>
          </a-tooltip>
        </a-descriptions-item>
        <a-descriptions-item label="多环境" v-if="typeof formData?.envSwitch != 'undefined'">
          <a-switch v-model:checked="formData.envSwitch" :checkedValue="1" :unCheckedValue="0" checked-children="启用"
            un-checked-children="关" />

          <a-tooltip>
            <template #title>
              <p> 开启多环境功能，存量数据会划分到名为 Default 的生产环境下，从接口拉取配置可以指定环境名</p>
            </template>
            <span class="tip">
              <QuestionCircleOutlined />
            </span>
          </a-tooltip>
        </a-descriptions-item>
      </a-descriptions>
    </a-card>

    <RoleView />
    <CustomUsers />
  </a-spin>
</template>

<script lang="ts" setup>
import { useRoute, useRouter } from 'vue-router'
import { apiFind, apiDelete, apiSave } from '@/api/project-service'
import { reactive, ref, watch, createVNode } from 'vue';
import { ProjectStruct } from '@/interface/Project';
import { QuestionCircleOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';
import ZSelect from '@/components/z-select'
import RoleView from './role.vue'
import CustomUsers from './customUsers.vue'

const route = useRoute()
const router = useRouter()
const formData = ref<ProjectStruct>()
const loading = ref(false)
enum OperateCMD {
  show, edit
}
const command = ref(OperateCMD.show)

watch(() => route.params, (val) => {
  if (val?.id) {
    let body: any = {
      appId: val.id as string
    }
    loading.value = true
    apiFind({ body }).then(res => {
      if (res.success && res.data.length > 0) {
        formData.value = res.data[0]
        pullSwitch.value = formData.value?.pullSwitch == 1
      }
    }).finally(() => {
      loading.value = false
    })
  }
}, { immediate: true, deep: true })

/** ============= 配置拉取签名 ============= */
const pullSwitch = ref(true)
const onPullSwitch = () => {
  let content = '启用签名认证后，所有拉取配置的接口都必须携带签名信息，否则将拉取数据失败。'
  if (pullSwitch.value) {
    content = '关闭签名认证后，拉取配置的接口将不再进行接口签名的校验。'
  }
  console.log(content, pullSwitch.value);
  Modal.confirm({
    title: '确认',
    icon: createVNode(ExclamationCircleOutlined),
    content,
    onOk: () => {
      pullSwitch.value = !pullSwitch.value

      let body: any = {
        id: formData.value?.id,
        pullSwitch: pullSwitch.value ? 1 : 0
      }
      loading.value = true
      apiSave(body).then(res => {
        if (!res.success) {
          console.log(res.msg);
        }
      }).catch(err => {
        console.error(err);
      }).finally(() => {
        loading.value = false
      })
    },
  })
}
/** ============= 配置拉取签名 ============= */

/** ============= 修改 ============= */
const formStore = reactive<{
  appName?: string
  projectManagers?: string[]
  description?: string
}>({
  appName: '',
  projectManagers: [],
  description: ''
})
const onEdit = () => {
  if (formData.value) {
    command.value = OperateCMD.edit
    formStore.appName = formData.value.appName
    formStore.projectManagers = (formData.value.projectManagers as string)?.split(';')
    formStore.description = formData.value.description
  }
}
/** 保存 */
const onSave = () => {
  if (!formStore?.appName || formStore?.projectManagers?.length == 0) {
    message.error('项目名、负责人不能为空！')
    return
  }
  if (!formData.value?.id) {
    return
  }

  let body: any = {
    id: formData.value?.id,
    appName: formStore.appName,
    projectManagers: formStore.projectManagers?.join(';'),
    description: formStore.description,
  }
  loading.value = true
  apiSave(body).then(res => {
    if (res.success) {
      message.success(`${formData?.value?.appName} 保存成功`)
      command.value = OperateCMD.show

      formData.value = res.data
      pullSwitch.value = formData.value?.pullSwitch == 1
    } else {
      message.error(res.msg)
    }
  }).finally(() => {
    loading.value = false
    formStore.appName = ''
    formStore.projectManagers = []
    formStore.description = ''
  })
}
/** ============= 修改 ============= */

/** 删除 */
const onDelete = () => {
  console.log(route.params, 'route.params.id=');
  Modal.confirm({
    title: '删除确认',
    icon: createVNode(ExclamationCircleOutlined),
    content: createVNode('div', { style: 'color:red;' }, '你确定要删除该项目？删除后无法恢复。'),
    onOk() {
      loading.value = true
      apiDelete([formData?.value?.id as string]).then(res => {
        if (res.success) {
          message.success(`${formData?.value?.appName} 删除成功`)
          router.push({ path: '/' })
        } else {
          message.error(res.msg)
        }
      }).finally(() => {
        loading.value = false
      })
    },
  });
}
</script>
<style lang='less' scoped>
.config-base {
  width: 100%;
  height: 100%;
}

.title {
  .title-span {
    font-size: 12px;
    color: #A6A6A6;
  }
}

.extra {
  .extra-span {
    margin-right: 10px;
    cursor: pointer;

    &:last-child {
      margin-right: 0;
    }
  }
}

.tip {
  display: inline-block;
  margin-left: 5px;
}
</style>

<style lang="less">
.config-base-des {

  .ant-descriptions-item-label,
  .ant-descriptions-item-content {
    line-height: 32px;
  }
}
</style>
