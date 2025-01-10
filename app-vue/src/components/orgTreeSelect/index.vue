<!-- 机构 树选择器 -->
<template>
  <div class="z-tree-select" ref="zTreeSelectRef">
    <Input type="text" v-show="false" v-model:value="eValue" style="width: 100%" />
    <a-form-item-rest>
      <Input class="input-ref" ref="inputRef" @focus="handleFocus" @click.stop="handleClick"
        :placeholder="formData?.title ? formData.title : placeholder" v-model:value="searchValue" :disabled="disabled"
        @input="onInput">
      <template #suffix v-if="allowClear">
        <CloseCircleOutlined class="close" v-show="formData?.title || searchValue" @click="onClose" />
      </template>
      </Input>
    </a-form-item-rest>
    <Teleport to="body">
      <div class="z-select-dropdown scrollbar" ref="zSelectDropdownRef" v-show="isFocus">
        <div v-if="loading" class="example" style="text-align: center">
          <Spin />
        </div>
        <div v-else-if="treeData.length <= 0" class="z-select-dropdown-empty">
          <Empty />
        </div>
        <Tree v-else-if="!loading && treeData.length > 0" :tree-data="treeData" @select="onSelect" @expand="onExpand"
          :selectedKeys="selectedKeys" :expanded-keys="expandedKeys" :auto-expand-parent="autoExpandParent">
          <template #title="{ title }">
            <div :title="title" v-if="searchValue"
              v-html="title.replace(new RegExp(searchValue, 'g'), '<span style=color:#f50>' + searchValue + '</span>')">
            </div>
            <div :title="title" v-else>
              {{ title }}
            </div>
          </template>
        </Tree>
      </div>
    </Teleport>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue'
import { Spin, Empty, Tree, Input, message } from 'ant-design-vue'
import { CloseCircleOutlined } from '@ant-design/icons-vue'
import { onClickOutside } from "@vueuse/core";
import { BaseParams } from '@/interface/base';
import { OrgStruct } from '@/interface/org';
import { useAppStore } from '@/store/app'
import { apiFind, apiFindWithID } from '@/api/system/org-service'
import { arrayToTree } from '@/utils/utils';

const props = defineProps({
  value: {
    type: null,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  placeholder: {
    type: String,
    default: '请选择',
  },
  /** 显示清除按钮 */
  allowClear: {
    type: Boolean,
    default: true
  },
})
const emit = defineEmits(['update:value', 'select'])

const appStore = useAppStore()
const listData = ref<Array<OrgStruct>>([])

const eValue = ref(props.value)
const treeData = ref<Array<any>>([])
const inputRef = ref()
const zTreeSelectRef = ref()
const zSelectDropdownRef = ref()
/** 初始化数据 避免重新请求 */
const initTreeData = ref<Array<any>>([])
const nodes = ref<Array<any>>([])
const loading = ref(false)
const isFocus = ref(false)
const searchValue = ref()
const aVelue = ref()
/** 当前选择的树 */
const formData = ref<any>({})
/** 指定选择树 */
const selectedKeys = ref<Array<any>>([])
/** 指定展开树 */
const expandedKeys = ref([])
const isSearch = ref(false)
const autoExpandParent = ref<boolean>(true);

const onExpand = (keys: any) => {
  expandedKeys.value = keys;
  autoExpandParent.value = false;
};

watch(() => props.value, (val) => {
  if (val) {
    eValue.value = val
  }
}, { immediate: true })

watch(() => isFocus.value, (val) => {
  searchValue.value = val ? aVelue.value : formData.value.title
}, { immediate: true })

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
        if (res.data.id == props.value) {
          selectedKeys.value = [res.data.id]
          formData.value = currentOrg
          setTimeout(() => {
            searchValue.value = currentOrg.title
            aVelue.value = undefined
            isFocus.value = false
            emit('update:value', formData.value.id)
            emit('select', formData.value) // 抛出事件 调用者使用
          }, 200)
        }
      }
    })
  }

  apiFind(body).then(res => {
    if (res.success) {
      const datas: Array<OrgStruct> = []
      res.data.map(v => {
        let obj = {
          ...v,
          title: v.name,
          key: v.id,
        }
        datas.push(obj)
        if (obj.id == props.value) {
          selectedKeys.value = [obj.id]
          formData.value = obj
          setTimeout(() => {
            searchValue.value = obj.name
            aVelue.value = undefined
            isFocus.value = false
            emit('update:value', formData.value.id)
            emit('select', formData.value) // 抛出事件 调用者使用
          }, 200)
        }

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


/** 树选择 */
const onSelect = (_selectedKeys: any, { node }: any) => {
  selectedKeys.value = _selectedKeys
  formData.value = node.dataRef
  setTimeout(() => {
    searchValue.value = node.dataRef.title
    aVelue.value = undefined
    isFocus.value = false
    emit('update:value', formData.value.id)
    emit('select', formData.value) // 抛出事件 调用者使用
  }, 200)
}

const handleClick = () => {
  isFocus.value = true
  zSelectDropdownRef.value.style.width = `${zTreeSelectRef.value.getBoundingClientRect().width}px`
  zSelectDropdownRef.value.style.left = `${zTreeSelectRef.value.getBoundingClientRect().left}px`
  zSelectDropdownRef.value.style.top = `${zTreeSelectRef.value.getBoundingClientRect().top + zTreeSelectRef.value.getBoundingClientRect().height
    }px`
  zSelectDropdownRef.value.style.borderTop = 'none'
}

/** 选择框事件 */
const handleFocus = () => {
  if (isSearch.value) {
    loading.value = true
    loading.value = false
    treeData.value.forEach((row) => {
      nodes.value[row.id] = row
    })
  }
  isSearch.value = false
  searchValue.value = aVelue.value
}
const onInput = () => {
  aVelue.value = searchValue.value
}

const onClose = () => {
  selectedKeys.value = []
  formData.value = undefined
  searchValue.value = undefined
  emit('update:value', undefined)
  emit('select', undefined) // 抛出事件 调用者使用
}


onClickOutside(zSelectDropdownRef, () => {
  isFocus.value = false
  if (formData.value) {
    searchValue.value = formData.value.title
  }
});

</script>
<style lang="less" scoped>
.z-tree-select {
  position: relative;
  width: 100%;

  .input-ref {
    width: 100%;
    height: 100%;
    appearance: none;

    &.input-ref-p {
      ::v-deep(input.ant-input) {
        cursor: pointer;
      }
    }


    &:focus {
      outline: none;
    }
  }

  .close {
    cursor: pointer;
    opacity: 0;
  }

  &:hover {
    .close {
      opacity: 1;
    }
  }
}

.z-select-dropdown {
  font-size: 14px;
  max-height: 400px;
  left: 0;
  position: fixed;
  padding: 8px 4px;
  z-index: 9999;
  color: #000000d9;
  background-color: #fff;
  transition: all 0.5s;
  box-shadow: 0 3px 6px -4px #0000001f, 0 6px 16px #00000014, 0 9px 28px 8px #0000000d;

  ::v-deep(.ant-tree) {

    .ant-tree-treenode {
      width: 100%;

      .ant-tree-node-content-wrapper {
        width: 100%;
      }
    }
  }
}

.scrollbar {
  &::-webkit-scrollbar {
    /*滚动条整体样式*/
    width: 4px;
    /*高宽分别对应横竖滚动条的尺寸*/
    height: 5px;
    // display: none
    background: transparent;
  }

  &::-webkit-scrollbar-thumb {
    /*滚动条里面小方块*/
    border-radius: 10px;
    -webkit-box-shadow: inset 0 0 5px transparent;
    background: transparent;
    transition: all .5s; //无效
  }

  &::-webkit-scrollbar-track {
    /*滚动条里面轨道*/
    // -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
    border-radius: 5px;
    background: transparent;
  }

  &::-webkit-scrollbar-corner {
    background-color: transparent;
  }

  &:hover {
    /* 兼容火狐 */
    scrollbar-color: rgb(223, 223, 223) #F5F5F5;
    scrollbar-width: 6px;
    scrollbar-track-color: transparent;
    -ms-scrollbar-track-color: transparent;

    &::-webkit-scrollbar-thumb {
      // display: block;
      background: rgba(24, 137, 241, 0.6);
      -webkit-box-shadow: inset 0 0 5px transparent;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }

    &::-webkit-scrollbar-corner {
      background-color: transparent;
    }
  }

  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-color: transparent transparent;
  scrollbar-track-color: transparent;
  -ms-scrollbar-track-color: transparent;
}
</style>
