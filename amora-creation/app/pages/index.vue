<template>
  <div class="page-container">
    <Header />

    <main>
      <ProductGrid />
    </main>

    </div>
</template>

<script lang="ts">
import Header from '../components/header.vue';
import ProductGrid from '../components/productGrid.vue';

export default {
  components: {
    Header,
    ProductGrid
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