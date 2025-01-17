<!-- 配置中心 -->
<template>
  <div class="content">
    <nav class="left-menu"></nav>

    <div class="detail-container">
      <RouteView />
    </div>
  </div>
</template>

<script lang="ts" setup>
import RouteView from '@/components/layouts/route-view'

</script>
<style lang='less' scoped>
.content {
  width: 100%;
  height: 100%;
  display: flex;

  .left-menu {
    width: 60px;
    height: 100%;
  }

  .detail-container {
    flex: 1 1 0;
    width: 0;
    height: 100%;
    overflow: auto;
    box-sizing: border-box;
    padding: 10px 10px;
  }
}
</style>
