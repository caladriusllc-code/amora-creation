<template>
  <div class="page-container">
    <Mainheader theme="black"/>
    <main class="main-layout">
      <productsCategory title="Catégories de produits"/>
    </main>
    <footerSection/>
  </div>
</template>

<script lang="ts">
import Mainheader from '../../components/navigator/header.vue';
import heroSection from '../../components/layout/heroSection.vue';
import productsCategory from '../../components/layout/ProductsCategory.vue'
import productGrid from '../../components/layout/productGrid.vue';
import footerSection from '~/components/layout/footerSection.vue';

export default {
  components: {
    Mainheader,
    heroSection,
    productsCategory,
    productGrid,
    footerSection
  },
  setup() {
    
    return {
      
    };
  }
}
</script>

<style scoped>
.page-container {
  background-color: #ffffff;
  min-height: 100vh;
}
</style>