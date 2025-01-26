<!-- 自定义用户 -->
<template>
  <a-card style="margin-top: 15px;">
    <template #title>
      <div class="title">
        <span style="margin-right: 5px;">自定义用户</span>
        <a-tooltip>
          <template #title>
            <p> 自定义用户的用途：</p>
            <p>1）开启“配置拉取签名”后，客户端须使用自定义用户做签名</p>
            <p>2）使用管理API时，把自定义用户加入角色列表来控制允许操作哪些分组</p>
          </template>
          <span class="tip">
            <QuestionCircleOutlined />
          </span>
        </a-tooltip>
        <span class="add-user-ms" @click="operateFn">新建用户</span>
      </div>
    </template>
    <BaseTable :columns="columns" :dataSource="listData" :pagination="pagination" :loading="loading"
      @change="handleTableChange" bordered class="table-list">
      <template #bodyCell="{ column, record }">
        <div v-if="column.dataIndex === 'operation'">
          <a-button class="options-btn" size="small" @click="operateFn(record, OperateCMD.edit)">编辑 </a-button>
          <a-popconfirm title="是否删除该数据?" ok-text="确认" cancel-text="取消" @confirm="toDelete(record)">
            <a-button class="options-btn" danger size="small">删除</a-button>
          </a-popconfirm>
        </div>
      </template>
    </BaseTable>
  </a-card>

  <Modal v-model:open="visible" title="添加自定义用户" :destroyOnClose="true" :width="500" :mask="false" @ok="handleOk">
    <a-form :model="formState" ref="formRef" :label-col="{ style: { width: '120px' } }" autocomplete="off">
      <a-form-item label="用户名" name="userName" :rules="[{ required: true, message: '请输入自定义用户吗' }]">
        <a-form-item-rest>
          <a-input-group compact>
            <a-input :style="{ width: '85px' }" value="Config_" :disabled="true" />
            <a-input :style="{ width: 'calc(100% - 85px)' }" v-model:value="formState.userName" :maxlength="25"
              placeholder="请输入自定义用户吗" />
          </a-input-group>
        </a-form-item-rest>
      </a-form-item>
      <a-form-item label="用户ID(userId)" name="userId">
        <a-input v-model:value="formState.userId" :disabled="true" placeholder="后台自动生成" />
      </a-form-item>
      <a-form-item label="密钥(secretKey)" name="secretKey">
        <a-input v-model:value="formState.secretKey" :disabled="true" placeholder="后台自动生成" />
      </a-form-item>
    </a-form>
  </Modal>
</template>

<script lang="ts" setup>
import { QuestionCircleOutlined } from '@ant-design/icons-vue';
import { reactive, ref, watch } from 'vue';
import { apiFind, apiDelete } from '@/api/role-service';
import BaseTable from '@/components/base-table';
import { CustomUser } from '@/interface/Role';
import { useManage, OperateCMD } from '@/hooks/useManage';
import { BaseParams } from '@/interface/base';
import { message, Modal } from 'ant-design-vue';

const listData = ref<Array<CustomUser>>([])
const loading = ref(false)
const columns = [
  {
    title: '用户名',
    dataIndex: 'userName',
    align: "left",
  },
  {
    title: '用户ID(userId)',
    dataIndex: 'userId',
    align: "left",
  },
  {
    title: '密钥(secretKey)',
    dataIndex: 'secretKey',
    align: "left",
  },
  {
    title: '状态',
    dataIndex: 'enableStatus',
    align: "left",
    customRender: (text: any) => {
      return text == 1 ? '已启用' : '禁用'
    }
  },
  {
    title: '操作',
    dataIndex: 'operation',
    align: "left",
  }
]

const { pagination, total, handleTableChange, visible, formData, goBack, route, operateFn } = useManage(doQuery)

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

/** =========== 新建 ====================== */
const formState = reactive<CustomUser>({
  userName: '',
  enableStatus: 1,
});
const formRef = ref()
const handleOk = (e: MouseEvent) => {
  formRef.value.validate().then(() => {
    let data = {
      appId: route.params?.id,
      ...formState
    }
    console.log(data);
    doSave(data)
  })
};
const doSave = (data: any) => {
  // apiSave(data).then(res => {
  //   if (res.success) {
  //     message.success('新增成功')
  //     emit('close', {
  //       ...data,
  //     })
  //   } else {
  //     message.error(res.msg)
  //   }
  // }).catch(err => {
  //   console.error(err)
  // })
}
/** =========== 新建 ====================== */


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
.add-user-ms {
  cursor: pointer;
  color: rgb(0, 82, 217);
  margin-left: 10px;
  font-size: 14px;
  font-weight: 400;
}
</style>
