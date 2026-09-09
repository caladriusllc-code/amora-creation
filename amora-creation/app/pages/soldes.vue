<template>
  <div class="page-container">
    <Mainheader theme="black" @toggle-cart="toggleCart"/>
    <div class="dis-section">
      <discountProductGrid @addToCart="showNotificationPopup"/>
    </div>
    <footerSection/>
    <cartModale/>
    <notifications
      :key="notificationKey"
      :visible="showNotification"
      @close="showNotification = false"
    />
  </div>
</template>

<script lang="ts">
import { ref, nextTick } from 'vue';
import Mainheader from '../components/navigator/header.vue'
import discountProductGrid from '~/components/layout/discountProductGrid.vue';
import footerSection from '~/components/layout/footerSection.vue';
import cartModale from '~/components/modale/cartModale.vue';
import notifications from '../components/tools/notifications.vue';

export default {
  components: {
    Mainheader,
    discountProductGrid,
    footerSection,
    cartModale,
    notifications
  },
  setup(){

    const isCartOpen = ref<boolean>(false);

    function toggleCart() {
      isCartOpen.value = !isCartOpen.value;
    }

    // ManageNotifications

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

    return{
      isCartOpen,
      showNotification,
      notificationKey,
      notificationTimer,
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