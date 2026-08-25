<template>
  <div class="page-container">
    <Mainheader theme="black" @toggle-cart="toggleCart" />
    <collectionWithProducts />
    <FooterSection />
    <cartModale :isOpen="isCartOpen" @close="toggleCart" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Mainheader from '../../components/navigator/header.vue'
import collectionWithProducts from '../../components/layout/collectionWithProducts.vue'
import FooterSection from '../../components/layout/footerSection.vue'
import cartModale from '../../components/modale/cartModale.vue'

const isCartOpen = ref<boolean>(false)

const toggleCart = () => {
  isCartOpen.value = !isCartOpen.value
}
</script>

<style scoped>
.page-container {
  background-color: #ffffff;
  min-height: 100vh;
}
</style>
