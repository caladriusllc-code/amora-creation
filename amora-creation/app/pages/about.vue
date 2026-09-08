<template>
    <div class="page-container">
        <Mainheader @toggle-cart="toggleCart"/>
            <main>
                <aboutUsSection />
            </main>
        <footerSection/>
    </div>
</template>

<script lang="ts">
import { nextTick, ref } from 'vue';


import Mainheader from '../components/navigator/header.vue'
import aboutUsSection from '~/components/layout/aboutUsSection.vue';
import footerSection from '~/components/layout/footerSection.vue';
export default {
  components: {
    Mainheader,
    aboutUsSection,
    footerSection,
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