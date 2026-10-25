<template>
  <div class="main-layout">
    <Head>
      <title>Amora création - Détail de produit</title>
      <meta name="description" content="Gotics Business & Web Analytics Dashboard" />
    </Head>
    <Mainheader theme="dark"/>
    <productDetail @addToCart="toggleCart"/>
    <cartModale :isOpen="isCartOpen" @close="toggleCart"/>
    <footerSection />
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import productDetail from '../components/layout/productDetail.vue'
import Mainheader from '../components/navigator/header.vue'
import cartModale from '../components/modale/cartModale.vue'
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
