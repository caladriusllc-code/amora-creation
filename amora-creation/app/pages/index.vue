<template>
  <div class="page-container">
    <Mainheader @toggle-cart="toggleCart"/>
    <main>
      <heroSection  />
      <productsCategory title="Catégories de produits"/>
      <productGrid 
        title="Nos produits les plus demandés"
        subtitle="Découvrez nos produits les plus demandés"
        :max-products="7"
        show-discover-more
        @add-to-cart="showNotificationPopup"
      />
      <discountProductGrid 
        title="Nos produits en soldes"
        subtitle="Découvrez nos produits en solde"
      />
    </main>
    <footerSection/>
    <cartModale :isOpen="isCartOpen" @close="toggleCart"/>
    <notifications
      :key="notificationKey"
      :visible="showNotification"
      @close="showNotification = false"
    />
  </div>
</template>

<script lang="ts">
import { nextTick, ref } from 'vue';


import Mainheader from '../components/navigator/header.vue'
import heroSection from '../components/layout/heroSection.vue';
import productsCategory from '../components/layout/ProductsCategory.vue'
import collectionSection from '../components/layout/collectionSection.vue'
import productGrid from '../components/layout/productGrid.vue';
import discountProductGrid from '~/components/layout/discountProductGrid.vue';
import footerSection from '~/components/layout/footerSection.vue';
import cartModale from '../components/modale/cartModale.vue';
import notifications from '~/components/tools/notifications.vue';

export default {
  components: {
    Mainheader,
    heroSection,
    collectionSection,
    productsCategory,
    productGrid,
    discountProductGrid,
    footerSection,
    cartModale,
    notifications
  },
  setup() {
    const isCartOpen = ref<boolean>(false);
    const showNotification = ref<boolean>(false);
    const notificationKey = ref<number>(0);
    let notificationTimer: ReturnType<typeof setTimeout> | null = null;

    function toggleCart() {
      isCartOpen.value = !isCartOpen.value;
    }

    function showNotificationPopup(){
      if (notificationTimer) {
        clearTimeout(notificationTimer);
      }

      notificationKey.value += 1;
      showNotification.value = false;

      nextTick(() => {
        showNotification.value = true;
        notificationTimer = setTimeout(() => {
          showNotification.value = false;
        }, 2500);
      });
    }

    return {
      isCartOpen,
      showNotification,
      notificationKey,
      toggleCart,
      showNotificationPopup
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