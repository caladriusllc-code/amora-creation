<template>
  <div class="page-container">
    <Mainheader @toggle-cart="toggleCart"/>
    <main>
      <heroSection />
      <productsCategory title="Catégories de produits"/>
      <productGrid 
        title="Nos produits les plus demandés"
        subtitle="Découvrez nos produits les plus demandés"
      />
      <productGrid 
        title="Soldes d'été"
        subtitle="Découvrez nos produits en solde"
      />
    </main>
    <footerSection/>
    <cartModale 
      :isOpen="isCartOpen"
      @close="toggleCart"
    />
  </div>
</template>

<script lang="ts">
import Mainheader from '../../components/navigator/header.vue'
import heroSection from '../../components/layout/heroSection.vue';
import productsCategory from '../../components/layout/ProductsCategory.vue'
import collectionSection from '../../components/layout/collectionSection.vue'
import productGrid from '../../components/layout/productGrid.vue';
import footerSection from '~/components/layout/footerSection.vue';
import cartModale from '../../components/modale/cartModale.vue'

import { ref } from 'vue'

export default {
  components: {
    Mainheader,
    heroSection,
    collectionSection,
    productsCategory,
    productGrid,
    footerSection,
    cartModale
  },
  setup() {
    // State 
    const isCartOpen = ref<boolean>(false);

    // Computed properties
    function toggleCart(){
      isCartOpen.value = !isCartOpen.value;
      console.log("Vous avez ouvert la modale")
    }

    // Actions

    return{
      // State
      isCartOpen,
      // computed properties
      toggleCart,
      // Actions 
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