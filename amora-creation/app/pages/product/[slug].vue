<template>
  <div class="main-layout">
    <Mainheader theme="black" @toggle-cart="toggleCart"/>
    <productDetail @addToCart="toggleCart"/>
    <footerSection/>
    <cartModale :isOpen="isCartOpen" @close="toggleCart"/>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import productDetail from '../../components/layout/productDetail.vue'
import Mainheader from '../../components/navigator/header.vue'
import cartModale from '../../components/modale/cartModale.vue'
import footerSection from '~/components/layout/footerSection.vue';
export default {
  components:{
    productDetail,
    Mainheader,
    cartModale,
    footerSection
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
