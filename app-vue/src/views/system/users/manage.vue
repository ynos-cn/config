<!-- 用户管理 -->
<template>
  <div class="manage" v-show="command === OperateCMD.showList">
    <BaseCard title="用户管理">
      <BaseSearch :config="searchConfig" @search="onSearch">
      </BaseSearch>
    </BaseCard>

    <div class="list-table">
      <div class="btns">
        <a-button class="btns-btn" @click="operateFn(null, OperateCMD.new)" type="primary">新增</a-button>
        <a-popconfirm title="是否删除这些数据?" ok-text="确认" cancel-text="取消" @confirm="toDelete(getSelectedRowKeys)">
          <a-button class="btns-btn" danger :disabled="getSelectedRowKeys.length <= 0">批量删除</a-button>
        </a-popconfirm>
      </div>
      <div class="table">
        <BaseTable :columns="columns" :dataSource="listData" :pagination="pagination" :loading="loading"
          @change="handleTableChange" bordered class="table-list" :rowSelection="rowSelection">
          <template #bodyCell="{ column, record }">
            <div v-if="column.dataIndex === 'operation'">
              <a-button class="options-btn" size="small" @click="operateFn(record, OperateCMD.edit)">编辑 </a-button>
              <a-button class="options-btn" size="small" @click="operateFn(record, OperateCMD.details)">查看 </a-button>
              <a-popconfirm title="是否删除该数据?" ok-text="确认" cancel-text="取消" @confirm="toDelete(record)">
                <a-button class="options-btn" danger size="small">删除</a-button>
              </a-popconfirm>
            </div>
          </template>
        </BaseTable>
      </div>
    </div>
  </div>


  <div class="modify" v-if="visible">
    <BaseCard :title="`用户管理${formData?.name ? `- ${formData?.name}` : ''}`">
      <template #addonAfter>
        <RollbackOutlined style="cursor: pointer;" @click="goBack(false)" title="返回" />
      </template>
      <Details :p-form-data="formData" v-if="command == OperateCMD.details" />
      <Modify :p-form-data="formData" @close="goBack" :edit-type="command" v-else />
    </BaseCard>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import BaseCard from '@/components/base-card'
import BaseSearch from '@/components/base-search'
import BaseTable from '@/components/base-table'
import { SearchConfig } from '@/components/base-search/interface'
import { OperateCMD, useManage } from '@/hooks/useManage'
import { useRowSelection } from '@/hooks/useTable'
import { RollbackOutlined } from '@ant-design/icons-vue'
import Modify from './modify.vue'
import Details from './details.vue'
import { apiDelete, apiFind } from '@/api/system/user-service'
import { message } from 'ant-design-vue'
import { BaseParams } from '@/interface/base'
import { UserStruct } from '@/interface/user'

const listData = ref<Array<UserStruct>>([])
const loading = ref(false)
const searchConfig: Array<SearchConfig> = [
  {
    label: '姓名',
    key: 'name',
    type: 'a-input',
    placeholder: '输入姓名搜索',
  },
  {
    label: '手机号码',
    key: 'phone',
    type: 'a-input',
    placeholder: '输入手机号码搜索',
  },
]
const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    align: 'center',
    ellipsis: true,
    width: 70,
  },
  {
    title: '姓名',
    dataIndex: 'name',
    align: 'center',
    ellipsis: true,
  },
  {
    title: '手机号码',
    dataIndex: 'phone',
    align: 'center',
    ellipsis: true,
  },
  {
    title: '职位',
    dataIndex: 'position',
    align: 'center',
    ellipsis: true,
  },
  {
    title: '入职时间',
    dataIndex: 'joinTime',
    align: 'center',
    ellipsis: true,
  },
  {
    title: '性别',
    dataIndex: 'sex',
    align: 'center',
    ellipsis: true,
    customRender: ({ text }) => {
      return text == 1 ? '男' : '女'
    }
  },
  {
    title: '邮箱',
    dataIndex: 'email',
    align: 'center',
    ellipsis: true,
  },
  {
    title: '所属机构',
    dataIndex: 'orgName',
    align: 'center',
    ellipsis: true,
  },
  {
    title: '状态',
    dataIndex: 'status',
    align: 'center',
    ellipsis: true,
    customRender: ({ text }) => {
      return text == 1 ? '可用' : '禁用'
    }
  },
  {
    title: '创建时间',
    dataIndex: 'createTime',
    align: 'center',
    ellipsis: true,
  },
  {
    title: '操作',
    dataIndex: 'operation',
    align: 'center',
    scopedSlots: { customRender: 'operation' },
    width: 230,
  },
]

const { onSearch, pagination, total, handleTableChange, searchData, operateFn, visible, command, formData, goBack } = useManage(doQuery)
const { rowSelection, getSelectedRowKeys, setCheckedKeys } = useRowSelection()

function doQuery() {
  let body: BaseParams<UserStruct> = {
    body: {
      ...searchData.value
    },
    page: pagination.value.current,
    limit: 10,
    sorter: { "updateTime": 1, id: 1 }
  }
  loading.value = true
  apiFind(body).then(res => {
    if (res.success) {
      res.data.map((v, i) => {
        Object.assign(v, {
          index: pagination.value.current
            ? (pagination.value.current - 1) * (pagination.value.pageSize ? pagination.value.pageSize : 10) + (i + 1)
            : i + 1,
        })
      })
      listData.value = res.data
      total.value = res.total
    } else {
      message.error(res.msg)
    }
  }).finally(() => {
    loading.value = false
  })
}
doQuery()

const toDelete = (listData: Array<any> | any) => {
  let sids: Array<string> = []
  if (listData instanceof Array) {
    listData.forEach((row) => {
      sids.push(row?.id ? row.id : row)
    })
  } else {
    sids.push(listData.id)
  }
  apiDelete(sids).then((result) => {
    if (result.success) {
      message.success('删除成功')
      setCheckedKeys([])
      doQuery()
      /* 计算是否是最后一页 */
      let num = total.value % pagination.value.pageSize
      if (sids.length == num || sids.length == pagination.value.pageSize) {
        pagination.value.current = pagination.value.current - 1
      }
    } else {
      message.error(result.message)
    }
  })
}

</script>
<style lang='less' scoped>
.manage {
  padding: 16px;
  width: 100%;
  height: 100%;

  .list-table {
    width: 100%;
    background: white;
    box-shadow: 0 0 10px #c5c5c5;
    overflow: hidden;
    border-radius: 5px;
    margin-top: 20px;
    padding: 10px;


    .btns {
      margin: 5px 0;
      padding-bottom: 5px;

      .btns-btn {
        margin-right: 5px;
      }

      .sort {
        .sort-btn {
          margin: 0 5px;
          cursor: pointer;
          font-size: 16px;
        }
      }
    }

  }

  .table {
    overflow: hidden;

    .options-btn {
      margin-left: 5px;

      &:first-child {
        margin-left: 0;
      }
    }
  }
}

.modify {
  padding: 16px;
  width: 100%;
  height: 100%;
}
</style>
