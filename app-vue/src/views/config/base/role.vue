<!-- 分角色权限 -->
<template>
  <a-card style="margin-top: 15px;">
    <template #title>
      <div class="title">
        <span style="margin-right: 5px;">分角色权限</span>
        <a-tooltip>
          <template #title>
            <p> 对权限类型的说明：</p>
            <p> 1）查看配置。可查看配置项，不可修改和发布配置，不能更改分组的设置</p>
            <p>2）编辑配置。对配置项的权限，细分为：添加、修改、删除、发布，可多选。发布任务需要分组管理员或项目负责人审批。注意：审批发布权限点是指优先审批人列表，会覆盖分组或项目的负责人权限</p>
            <p>3）管理分组。对分组有所有权限，包含审批发布任务 项目负责人具备项目级的所有权限</p>
          </template>
          <span class="tip">
            <QuestionCircleOutlined />
          </span>
        </a-tooltip>
      </div>
    </template>
    <div class="role-ms">
      <div class="role-ms-item">
        <span>我的角色</span>
        <span>xxx;</span>
      </div>
      <div class="role-ms-item">
        <span>所有角色</span>
        <span style="cursor: pointer; color: #0052d9;" @click="onAddRole">新建角色</span>
      </div>
    </div>
    <BaseTable :columns="columns" :dataSource="listData" :pagination="pagination" :loading="loading"
      @change="handleTableChange" bordered class="table-list">
      <template #bodyCell="{ column, record }">
        <div v-if="column.dataIndex == 'persons'">
          <div v-for="item in record.persons">
            {{ item.type == 1 ? 'OA用户' : "OA组织" }}：{{ item.names }}
          </div>
        </div>
        <div v-if="column.dataIndex == 'permissionTypes'">
          {{ getPermissionTypes(record.permissionTypes) }}
        </div>
        <div v-if="column.dataIndex === 'operation'">
          <!-- <a-button class="options-btn" size="small" @click="operateFn(record, OperateCMD.edit)">编辑 </a-button> -->
          <a-popconfirm title="是否删除该数据?" ok-text="确认" cancel-text="取消" @confirm="toDelete(record)">
            <a-button class="options-btn" danger size="small">删除</a-button>
          </a-popconfirm>
        </div>
      </template>
    </BaseTable>
  </a-card>

  <Modal v-model:open="visible" title="创建项目" :width="888" :mask="false" @ok="handleOk">
    <RoleModify ref="roleModifyRef" @close="goBack" />
  </Modal>
</template>

<script lang="ts" setup>
import { QuestionCircleOutlined } from '@ant-design/icons-vue';
import { ref, watch } from 'vue';
import { apiFind, apiDelete } from '@/api/role-service';
import BaseTable from '@/components/base-table';
import { RoleStruct } from '@/interface/Role';
import { useManage } from '@/hooks/useManage';
import { BaseParams } from '@/interface/base';
import { message, Modal } from 'ant-design-vue';
import { PermissionType } from './setting'
import RoleModify from './roleModify.vue'

const listData = ref<Array<RoleStruct>>([])
const loading = ref(false)
const columns = [
  {
    title: '角色名称',
    dataIndex: 'name',
    align: "left",
  },
  {
    title: '人员列表',
    dataIndex: 'persons',
    align: "left",
  },
  {
    title: '配置分组名',
    dataIndex: 'object',
    align: "left",
  },
  {
    title: '权限类型',
    dataIndex: 'permissionTypes',
    align: "left",
  },
  {
    title: '操作',
    dataIndex: 'operation',
    align: "left",
  }
]

const { pagination, total, handleTableChange, visible, command, formData, goBack, route } = useManage(doQuery)

function doQuery() {
  if (!route.params?.id) {
    return
  }
  let body: BaseParams<any> = {
    body: {
      appId: route.params?.id
    },
    page: pagination.value.current,
    limit: pagination.value.pageSize,
    sorter: { "updateTime": 1, id: 1 }
  }
  loading.value = true
  apiFind(body).then(res => {
    if (res.success) {
      listData.value = res.data
      total.value = res.total
    } else {
      message.error(res.msg)
    }
  }).finally(() => {
    loading.value = false
  })
}

watch(() => route.params, (val) => {
  if (val?.id) {
    doQuery()
  }
}, { immediate: true, deep: true })

/** =========== 新建角色 ====================== */
const roleModifyRef = ref()
const onAddRole = () => {
  visible.value = true
}
const handleOk = (e: MouseEvent) => {
  roleModifyRef.value.onFinish()
};
/** =========== 新建角色 ====================== */

const getPermissionTypes = (permissionTypes) => {
  let strArr: Array<string> = []
  let arr: Array<string> = []
  if (typeof permissionTypes === 'string') {
    arr = permissionTypes.split(';')
  }
  if (Array.isArray(permissionTypes)) {
    arr = permissionTypes
  }
  arr.map(v => {
    let label = PermissionType.find(item => item.name === v)?.label
    if (label) {
      strArr.push(label)
    }
  })

  return strArr.join(';')
}


/** =========== 删除 ====================== */
const toDelete = (listData: Array<any> | any) => {
  let sids: Array<string> = []
  if (listData instanceof Array) {
    listData.forEach((row) => {
      sids.push(row?.id ? row.id : row)
    })
  } else {
    sids.push(listData.id)
  }
  loading.value = true
  apiDelete(sids).then((result) => {
    if (result.success) {
      message.success('删除成功')
      /* 计算是否是最后一页 */
      let num = total.value % pagination.value.pageSize
      if (sids.length == num || sids.length == pagination.value.pageSize) {
        pagination.value.current = pagination.value.current - 1
      }
      doQuery()
    } else {
      message.error(result.msg)
    }
  }).catch((error) => {
    console.error(error)
    loading.value = false
  })
}
/** =========== 删除 ====================== */

</script>
<style lang='less' scoped>
.role-ms {
  display: flex;
  flex-direction: column;

  .role-ms-item {
    line-height: 32px;

    span {
      display: inline-block;
      margin-right: 10px;

      &:last-child {
        margin-right: 0;
      }
    }
  }
}
</style>
