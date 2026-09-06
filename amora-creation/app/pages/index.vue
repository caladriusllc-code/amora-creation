<template>
  <div class="page-container">
    <Mainheader @toggle-cart="toggleCart"/>
    <main>
      <heroSection />
      <productsCategory title="Catégories de produits"/>
      <productGrid 
        title="Nos produits les plus demandés"
        subtitle="Découvrez nos produits les plus demandés"
        :max-products="7"
        show-discover-more
      />
      <discountProductGrid 
        title="Nos produits en soldes"
        subtitle="Découvrez nos produits en solde"
      />
    </main>
    <footerSection/>
    <cartModale :isOpen="isCartOpen" @close="toggleCart"/>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';


import Mainheader from '../components/navigator/header.vue'
import heroSection from '../components/layout/heroSection.vue';
import productsCategory from '../components/layout/ProductsCategory.vue'
import collectionSection from '../components/layout/collectionSection.vue'
import productGrid from '../components/layout/productGrid.vue';
import discountProductGrid from '~/components/layout/discountProductGrid.vue';
import footerSection from '~/components/layout/footerSection.vue';
import cartModale from '../components/modale/cartModale.vue'

export default {
  components: {
    Mainheader,
    heroSection,
    collectionSection,
    productsCategory,
    productGrid,
    discountProductGrid,
    footerSection,
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
.page-container {
  background-color: #ffffff;
  min-height: 100vh;
}
</style>