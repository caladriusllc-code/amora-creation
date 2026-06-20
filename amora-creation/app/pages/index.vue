<template>
  <div class="page-container">
    <Mainheader/>
    <main>
      <heroSection />
    </main>
  </div>
</template>

<script lang="ts">
import Mainheader from '../components/navigator/header.vue'
import ProductGrid from '../components/layout/productGrid.vue';
import heroSection from '../components/layout/heroSection.vue';

export default {
  components: {
    Mainheader,
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