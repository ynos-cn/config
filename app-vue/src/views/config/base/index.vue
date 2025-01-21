<!-- 信息 -->
<template>
  <a-card>
    <template #title>
      <div class="title">
        <span>基础信息</span>
        <span class="title-span">({{ formData?.creator }} 创建于 {{ formData?.createTime }})</span>
      </div>
    </template>
    <template #extra>
      <div class="extra">
        <span class="extra-span" style="color: #0052d9;">编辑</span>
        <span class="extra-span" style="color: #ff3e00;" @click="onDelete">删除项目</span>
      </div>
    </template>
    <a-descriptions :column="2">
      <a-descriptions-item label="项目名">{{ formData?.appName }}</a-descriptions-item>
      <a-descriptions-item label="项目ID(Appid)">{{ formData?.appId }}</a-descriptions-item>
      <a-descriptions-item label="负责人">
        {{ formData?.projectManagers }}
        <a-tooltip>
          <template #title>负责人具有项目所有权限（如修改负责人列表、设置分角色权限等）</template>
          <span class="tip">
            <QuestionCircleOutlined />
          </span>
        </a-tooltip>
      </a-descriptions-item>
      <a-descriptions-item label="部门">{{ formData?.orgName }}</a-descriptions-item>
      <a-descriptions-item label="描述">{{ formData?.description }}</a-descriptions-item>
      <a-descriptions-item label="配置拉取签名" v-if="typeof formData?.pullSwitch != 'undefined'">
        <a-switch v-model:checked="formData.pullSwitch" :checkedValue="1" :unCheckedValue="0" checked-children="启用"
          un-checked-children="关" @change="onPullSwitch" />
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
</template>

<script lang="ts" setup>
import { useRoute, useRouter } from 'vue-router'
import { apiFind, apiDelete, apiSave } from '@/api/project-service'
import { ref, watch, createVNode } from 'vue';
import { ProjectStruct } from '@/interface/Project';
import { QuestionCircleOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';

const route = useRoute()
const router = useRouter()
const formData = ref<ProjectStruct>()

watch(() => route.params, (val) => {
  if (val?.id) {
    let body: any = {
      appId: val.id as string
    }
    apiFind({
      body
    }).then(res => {
      console.log(res, 'res');
      if (res.success && res.data.length > 0) {
        formData.value = res.data[0]
      }
    })
  }
}, { immediate: true, deep: true })

const onDelete = () => {
  console.log(route.params, 'route.params.id=');
  Modal.confirm({
    title: '删除确认',
    icon: createVNode(ExclamationCircleOutlined),
    content: createVNode('div', { style: 'color:red;' }, '你确定要删除该项目？删除后无法恢复。'),
    onOk() {
      apiDelete([formData?.value?.id as string]).then(res => {
        if (res.success) {
          message.success(`${formData?.value?.appName} 删除成功`)
          router.push({ path: '/' })
        } else {
          message.error(res.msg)
        }
      })
    },
  });
}

/** 配置拉取签名 */
const onPullSwitch = () => {
  console.log(formData.value?.pullSwitch);
  let body: any = {
    id: formData.value?.id, pullSwitch: formData.value?.pullSwitch as number
  }
  apiSave(body).then(res => {
    console.log(res, 'res');
  })
}
</script>
<style lang='less' scoped>
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
