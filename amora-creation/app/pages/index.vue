<template>
  <div class="page-container">
    <Mainheader/>
    <main>
      <heroSection />
      <productsCategory title="Catégories de produits"/>
    </main>
  </div>
</template>

<script lang="ts">
import Mainheader from '../components/navigator/header.vue'
import heroSection from '../components/layout/heroSection.vue';
import productsCategory from '../components/layout/ProductsCategory.vue'

export default {
  components: {
    Mainheader,
    heroSection,
    productsCategory
  },
  setup() {
    return {};
  }
}
</script>

<style scoped>
.page-container {
  background-color: #ffffff;
  min-height: 100vh;
}
</style>