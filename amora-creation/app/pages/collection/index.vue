<template>
  <div class="page-container">
    <Mainheader @toggle-cart="toggleCart" theme="light" />
    <main>
      <collectionSection />
    </main>
    <FooterSection />
    <cartModale :isOpen="isCartOpen" @close="toggleCart" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Mainheader from '../../components/navigator/header.vue'
import collectionSection from '../../components/layout/collectionSection.vue'
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
