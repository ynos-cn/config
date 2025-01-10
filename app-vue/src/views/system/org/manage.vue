<!-- 机构管理 -->
<template>
  <div class="manage org">
    <BaseCard title="机构管理" style="height: 100%;">
      <div class="org-content">
        <div class="org-content-left">
          <a-input-search v-model:value="searchValue" style="margin-bottom: 8px" placeholder="关键字搜索" />
          <a-tree :expanded-keys="expandedKeys" :auto-expand-parent="autoExpandParent" :tree-data="treeData"
            @expand="onExpand" @drop="onDrop" draggable @select="onSelect" class="org-content-left-tree">
            <template #title="{ dataRef, title }">
              <a-dropdown :trigger="['contextmenu']">
                <span v-if="title.indexOf(searchValue) > -1">
                  {{ title.substring(0, title.indexOf(searchValue)) }}
                  <span style="color: #f50">{{ searchValue }}</span>
                  {{ title.substring(title.indexOf(searchValue) + searchValue.length) }}
                </span>
                <span v-else>{{ title }}</span>
                <template #overlay>
                  <a-menu @click="({ key: menuKey }) => onContextMenuClick(dataRef, menuKey)">
                    <a-menu-item key="add">
                      <span>
                        <PlusSquareOutlined />
                        新增机构
                      </span>
                    </a-menu-item>
                    <a-menu-item key="delete" v-if="dataRef.isDelete != false">
                      <span style="color: red;">
                        <DeleteOutlined />
                        删除
                      </span>
                    </a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>

            </template>
          </a-tree>
        </div>
        <div class="org-content-right">
          <Modify :p-form-data="formData" :editType="command" @close="onClose" />
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script lang="ts" setup>
import { createVNode, ref, watch } from 'vue'
import BaseCard from '@/components/base-card'
import { ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { apiDelete, apiFind, apiFindWithID, apiUpdateOrg } from '@/api/system/org-service'
import { message, Modal } from 'ant-design-vue'
import { BaseParams } from '@/interface/base'
import { OrgStruct } from '@/interface/org'
import { arrayToTree } from '@/utils/utils'
import { useAppStore } from '@/store/app'
import { AntTreeNodeDropEvent } from 'ant-design-vue/es/tree'
import { DeleteOutlined, PlusSquareOutlined } from '@ant-design/icons-vue';
import Modify from './modify.vue'
import { OperateCMD } from '@/hooks/useManage'

const appStore = useAppStore()

const listData = ref<Array<OrgStruct>>([])
const loading = ref(false)

const command = ref(OperateCMD.details)

async function doQuery() {
  let body: BaseParams<OrgStruct | any> = {
    body: {},
    page: 1,
    limit: -1,
    sorter: { "createTime": 1 }
  }
  loading.value = true

  let currentOrg: OrgStruct
  if (appStore.userInfo?.orgId) {
    await apiFindWithID(appStore.userInfo?.orgId).then(res => {
      if (res.success) {
        currentOrg = {
          ...res.data,
          title: res.data.name,
          key: res.data.id,
          isDelete: false
        }
      }
    })
  }

  apiFind(body).then(res => {
    if (res.success) {
      const datas: Array<OrgStruct> = []
      res.data.map(v => {
        datas.push({
          ...v,
          title: v.name,
          key: v.id,
        })
      })
      if (currentOrg) {
        datas.unshift(currentOrg)
      }
      listData.value = JSON.parse(JSON.stringify(datas))
      treeData.value = arrayToTree<OrgStruct>(datas, 'orgId')
    } else {
      message.error(res.msg)
    }
  }).finally(() => {
    loading.value = false
  })
}
doQuery()

const formData = ref<OrgStruct>()
const onSelect = (_selectedKeys: any, { selectedNodes }: any) => {
  if (selectedNodes.length > 0) {
    formData.value = selectedNodes[0]
    command.value = OperateCMD.edit
  } else {
    formData.value = undefined
    command.value = OperateCMD.details
  }
}

const searchValue = ref('')
const expandedKeys = ref<(string | number)[]>([]);
const autoExpandParent = ref<boolean>(true);
const treeData = ref<Array<any>>([]);
const onExpand = (keys: any) => {
  expandedKeys.value = keys;
  autoExpandParent.value = false;
};

const getParentKey = (
  key: string | number,
  tree: Array<any>,
): string | number | undefined => {
  let parentKey;
  if (tree) {
    for (let i = 0; i < tree.length; i++) {
      const node = tree[i];
      if (node.children) {
        if (node.children.some(item => item.key === key)) {
          parentKey = node.key;
        } else if (getParentKey(key, node.children)) {
          parentKey = getParentKey(key, node.children);
        }
      }
    }
  }
  return parentKey;
};
watch(searchValue, value => {
  const expanded = listData.value
    .map((item: any) => {
      if (item.title.indexOf(value) > -1) {
        return getParentKey(item.key, treeData.value);
      }
      return null;
    })
    .filter((item, i, self) => item && self.indexOf(item) === i);
  expandedKeys.value = expanded as any;
  searchValue.value = value;
  autoExpandParent.value = true;
});

const onDrop = (info: AntTreeNodeDropEvent) => {
  const dropKey = info.node.key;
  const dragKey = info.dragNode.key;
  const dropPos = info.node.pos?.split('-') ?? [];
  const dropPosition = info.dropPosition - Number(dropPos[dropPos.length - 1]);
  const loop = (data: Array<any>, key: string | number, callback: any) => {
    data.forEach((item, index) => {
      if (item.key === key) {
        return callback(item, index, data);
      }
      if (item.children) {
        return loop(item.children, key, callback);
      }
    });
  };
  const data = [...treeData.value];

  Modal.confirm({
    title: '修改所属机构',
    icon: createVNode(ExclamationCircleOutlined),
    content: `确定要修改所属机构？`,
    onOk() {
      // Find dragObject
      let dragObj: any;
      let pObj: any
      loop(data, dragKey, (item: any, index: number, arr: Array<any>) => {
        arr.splice(index, 1);
        dragObj = item;
      });

      let saveData: any
      if (!info.dropToGap) {
        // Drop on the content
        loop(data, dropKey, (item: any) => {
          item.children = item.children || [];
          /// where to insert 示例添加到头部，可以是随意位置
          item.children.unshift(dragObj);
          pObj = item
        });
      } else if (
        (info.node.children || []).length > 0 && // Has children
        info.node.expanded && // Is expanded
        dropPosition === 1 // On the bottom gap
      ) {
        loop(data, dropKey, (item: any) => {
          item.children = item.children || [];
          // where to insert 示例添加到头部，可以是随意位置
          item.children.unshift(dragObj);
          pObj = item
        });
      } else {
        // 调整顺序
        let ar: Array<any> = [];
        let i = 0;
        let prObj: any;
        loop(data, dropKey, (item: any, index: number, arr: Array<any>) => {
          ar = arr;
          i = index;
          prObj = item
        });
        if (dropPosition === -1) {
          ar.splice(i, 0, dragObj);
        } else {
          ar.splice(i + 1, 0, dragObj);
        }
        saveData = {
          id: dragObj.id,
          orgId: prObj.orgId,
          orgName: prObj.orgName
        }
      }
      if (pObj) {
        saveData = {
          id: dragObj.id,
          orgId: pObj.id,
          orgName: pObj.name
        }
      }
      apiUpdateOrg(saveData).then(res => {
        if (res.success) {
          message.success('修改成功')
        } else {
          message.error(res.msg)
        }
      })

      treeData.value = data;
    },
  });
};

const onClose = (record: any) => {
  if (record) {
    doQuery()
  }
}

/**
 * 右键菜单
 * @param data 
 * @param menuKey 
 */
const onContextMenuClick = (data: OrgStruct, menuKey: string | number) => {
  if (menuKey == 'delete') {
    let ids: Array<string> = []
    if (data.id) {
      if (data.id === appStore.userInfo?.orgId) {
        message.error('不能删除当前机构')
        return
      }
      ids.push(data.id)
    }
    if (ids.length > 0) {
      apiDelete(ids).then(res => {
        if (res.success) {
          message.success('删除成功')
          doQuery()
        } else {
          message.error(res.msg)
        }
      })
    }
  } else if (menuKey == 'add') {
    if (data.id) {
      expandedKeys.value.push(data.id)
    }

    formData.value = {
      orgId: data.id,
      orgName: data.name,
      name: '',
      code: '',
      controllerName: '',
      controllerTel: ''
    }
    command.value = OperateCMD.new
  }
};

</script>
<style lang='less' scoped>
.manage {
  padding: 16px;
  width: 100%;
  height: 100%;

  .org-content {
    width: 100%;
    height: 100%;
    overflow: hidden;

    .org-content-left {
      width: 350px;
      height: 100%;
      float: left;
      border-right: 1px solid #ededed;
      padding: 0 10px;
    }

    .org-content-right {
      width: calc(100% - 350px);
      height: 100%;
      float: left;
      padding: 0 10px;
    }
  }
}

.modify {
  padding: 16px;
  width: 100%;
  height: 100%;
}
</style>
<style lang="less">
.org {
  .org-content {
    .org-content-left {
      .org-content-left-tree {
        height: calc(100% - 39px);
        overflow-y: auto;
      }
    }
  }
}
</style>
