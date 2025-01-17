<!-- 左侧菜单 -->
<template>
  <div class="menu">
    <div class="menu-item" v-for="item in menuList" :key="item.key"
      :class="[currentKey == item.key && 'menu-item-active']" @click="onGoMenu(item)">
      <div class="menu-item-icon">
        <component :is="item.icon" />
      </div>
      <div class="menu-item-text">{{ item.title }}</div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { HomeOutlined, ControlOutlined, ProfileOutlined } from '@ant-design/icons-vue';
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const menuList = [
  { title: '信息', icon: HomeOutlined, key: 'base' },
  { title: '配置', icon: ControlOutlined, key: 'list' },
  { title: '任务', icon: ProfileOutlined, key: 'task' },
]
const currentKey = ref('base')
const currentAppId = ref('')

watch(() => route.path, (newPath) => {
  let arr = newPath.split('/')
  let key = arr[arr.length - 1]
  currentAppId.value = arr[arr.length - 2]
  currentKey.value = key
}, { immediate: true, deep: true })

const onGoMenu = (record) => {
  router.push({
    path: `/${currentAppId.value}/${record.key}`,
  })
}

</script>
<style lang='less' scoped>
.menu {
  width: 100%;
  height: 100%;
  box-shadow: 1px 0 10px 0 rgba(0, 10, 41, .05), 4px 0 5px 0 rgba(0, 10, 41, .08), 2px 0 4px -1px rgba(0, 10, 41, .12);
  position: relative;
  font-size: 14px;
  background-color: #fff;

  .menu-item {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding-top: 15px;
    cursor: pointer;
    color: #666;

    &:hover,
    &.menu-item-active {
      color: #0052d9;
    }

    .menu-item-icon {
      font-size: 22px;
    }

    .menu-item-text {
      font-size: 14px;
      line-height: 26px;
    }
  }
}
</style>
