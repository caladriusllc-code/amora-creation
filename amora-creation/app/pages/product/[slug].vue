<template>
  <div class="main-layout">
    <Mainheader theme="dark" @toggle-cart="toggleCart"/>
    <productDetail @addToCart="toggleCart"/>
    <cartModale :isOpen="isCartOpen" @close="toggleCart"/>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import productDetail from '../../components/layout/productDetail.vue'
import Mainheader from '../../components/navigator/header.vue'
import cartModale from '../../components/modale/cartModale.vue'
export default {
  components:{
    productDetail,
    Mainheader,
    cartModale
  },
  setup() {
    const isCartOpen = ref<boolean>(false);

    function toggleCart() {
      isCartOpen.value = !isCartOpen.value;
    }

    return {
      isCartOpen,
      toggleCart
    }
  }
}
</script>

<style scoped>

</style>