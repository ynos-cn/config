<!--
 * @Description: 403
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2023-09-18 18:15:44
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-09-18 18:17:23
-->
<template>
  <Result status="403" title="403" style="background: none" sub-title="Sorry, you don't have access to this page.">
    <template #extra>
      <router-link to="/">
        <Button type="primary">Back Home</Button>
      </router-link>
    </template>
  </Result>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Result, Button } from 'ant-design-vue'

export default defineComponent({
  name: 'Exception403',
  components: { Result, Button },
  setup() {
    return {};
  },
});
</script>
