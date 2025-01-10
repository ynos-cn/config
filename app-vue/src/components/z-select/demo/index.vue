<template>
  <demo-sort>
    <Base />
    <Base1 />
    <Base2 />
    <Base3 />
    <Base4 />
  </demo-sort>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import Base from './basic.vue'
import Base1 from './basic1.vue'
import Base2 from './basic2.vue'
import Base3 from './basic3.vue'
import Base4 from './basic4.vue'
import MD from '../index.md'

export default defineComponent({
  MD,
  components: { Base, Base1, Base2, Base3, Base4 }
})
</script>