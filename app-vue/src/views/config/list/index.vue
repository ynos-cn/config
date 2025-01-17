<!-- 配置中心 -->
<template>
  <div class="container">
    <div class="grouping">
      分组
    </div>

    <div class="content">
      内容
    </div>
  </div>
</template>

<script lang="ts" setup>

</script>
<style lang='less' scoped>
.container {
  height: 100%;
  background-color: #fff;
  max-height: 100%;
  display: flex;

  .grouping {
    width: 288px;
    flex: 0 0 auto;
    align-items: stretch;
    position: relative;
    max-height: 100%;
    overflow: auto;
    background: #f1f2f5;
    border-radius: 3px;
  }

  .content {
    flex: 1;
    overflow: hidden;
  }

}
</style>
