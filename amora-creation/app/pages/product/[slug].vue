<template>
  <div class="main-layout">
    <Head>
      <title>Amora - {{ title }}</title>
      <meta name="description" content="Gotics Business & Web Analytics Dashboard" />
    </Head>
    <Mainheader theme="black" @toggle-cart="toggleCart"/>
    <productDetail @addToCart="toggleCart"/>
    <footerSection/>
    <cartModale :isOpen="isCartOpen" @close="toggleCart"/>
  </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

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
    const route = useRoute();
    const title = computed(()=>{
      const slug = route.params.slug;
      return slug;
    })

    const isCartOpen = ref<boolean>(false);

    function toggleCart() {
      isCartOpen.value = !isCartOpen.value;
    }

    return {
      route,
      title,
      isCartOpen,
      toggleCart
    }
  }
}
</script>

<style scoped>

</style>
