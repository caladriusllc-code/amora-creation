<template>
  <div class="page-container">
    <Mainheader/>
    <main>
      <heroSection />
      <productsCategory title="Catégories de produits"/>
      <productGrid 
        title="Nos produits les plus demandés"
        subtitle="Découvrez nos produits les plus demandés"
      />
      <discountProductGrid
        title="Soldes d'été"
        subtitle="Découvrez nos produits en solde"
      />
    </main>
    <footerSection/>
  </div>
</template>

<script lang="ts">
import Mainheader from '../components/navigator/header.vue'
import heroSection from '../components/layout/heroSection.vue';
import productsCategory from '../components/layout/ProductsCategory.vue'
import collectionSection from '../components/layout/collectionSection.vue'
import productGrid from '../components/layout/productGrid.vue';
import discountProductGrid from '~/components/layout/discountProductGrid.vue';
import footerSection from '~/components/layout/footerSection.vue';

export default {
  components: {
    Mainheader,
    heroSection,
    collectionSection,
    productsCategory,
    productGrid,
    discountProductGrid,
    footerSection
  }
}
</script>

<style scoped>
.page-container {
  background-color: #ffffff;
  min-height: 100vh;
}
</style>