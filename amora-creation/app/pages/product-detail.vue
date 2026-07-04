<template>
  <div class="main-layout">
    <Mainheader/>
    <productDetail/>
  </div>
</template>

<script>
import productDetail from '../components/layout/productDetail.vue'
import Mainheader from '../components/navigator/header.vue'
export default {
  components:{
    productDetail,
    Mainheader
  }
}
</script>

<style scoped>

</style>