<template>
  <div class="page-container">
    <Header />
    <main>
      <heroSection />
      <ProductGrid />
    </main>
  </div>
</template>

<script lang="ts">
import Header from '../components/header.vue';
import ProductGrid from '../components/productGrid.vue';
import heroSection from '../components/layout/heroSection.vue';

export default {
  components: {
    Header,
    ProductGrid,
    heroSection
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