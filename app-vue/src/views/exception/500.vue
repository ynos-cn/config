<!--
 * @Description: 500
 * @Version: 1.0
 * @Autor: jiajun.wu
 * @Date: 2023-09-18 18:15:44
 * @LastEditors: jiajun.wu
 * @LastEditTime: 2023-09-18 18:16:39
-->
<template>
  <Result status="500" title="500" style="background: none" sub-title="Sorry, the server is reporting an error.">
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
  name: 'Exception500',
  components: { Button, Result },
  setup() {
    return {};
  },
});
</script>
