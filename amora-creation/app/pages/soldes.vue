<template>
  <div class="page-container">
    <Mainheader theme="black" @toggle-cart="toggleCart"/>
    <div class="dis-section">
      <discountProductGrid/>
    </div>
    <footerSection/>
    <cartModale/>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import Mainheader from '../components/navigator/header.vue'
import discountProductGrid from '~/components/layout/discountProductGrid.vue';
import footerSection from '~/components/layout/footerSection.vue';
import cartModale from '~/components/modale/cartModale.vue';

export default {
  components: {
    Mainheader,
    discountProductGrid,
    footerSection,
    cartModale
  },
  setup(){

    const isCartOpen = ref<boolean>(false);

    function toggleCart() {
      isCartOpen.value = !isCartOpen.value;
    }

    return{
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

.dis-section{
  padding-top: 24px;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}
</style>