<template>
  <div class="main-layout">
    <Head>
      <title>Amora - {{ title }}</title>
      <meta name="description" content="Gotics Business & Web Analytics Dashboard" />
    </Head>
    <Mainheader theme="black" @toggle-cart="toggleCart"/>
    <productDetail @addToCart="handleProductAdded"/>
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
import { ref, computed, nextTick } from 'vue';
import { useRoute } from 'vue-router';

import productDetail from '../../components/layout/productDetail.vue'
import Mainheader from '../../components/navigator/header.vue'
import cartModale from '../../components/modale/cartModale.vue'
import footerSection from '~/components/layout/footerSection.vue';
import notifications from '~/components/tools/notifications.vue';
export default {
  components:{
    productDetail,
    Mainheader,
    cartModale,
    footerSection,
    notifications
  },
  setup() {
    const route = useRoute();
    const title = computed(()=>{
      const slug = route.params.slug;
      return slug;
    })

    const isCartOpen = ref<boolean>(false);

    function toggleCart() {
      isCartOpen.value = !isCartOpen.value;
    }

    function handleProductAdded() {
      isCartOpen.value = true;
      showNotificationPopup();
    }

    const showNotification = ref<boolean>(false);
    const notificationKey = ref<number>(0);
    let notificationTimer: ReturnType<typeof setTimeout> | null = null;

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
      route,
      title,
      isCartOpen,
      toggleCart,
      handleProductAdded,
      showNotification,
      notificationKey,
      notificationTimer,
      showNotificationPopup
    }
  }
}
</script>

<style scoped>

</style>
