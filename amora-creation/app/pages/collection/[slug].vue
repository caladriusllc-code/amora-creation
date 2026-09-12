<template>
  <div class="page-container">
    <Mainheader theme="light" @toggle-cart="toggleCart" />
    <collectionWithProducts  @add-to-cart="handleProductAdded"/>
    <FooterSection />
    <cartModale :isOpen="isCartOpen" @close="toggleCart" />
    <notifications
      :key="notificationKey"
      :visible="showNotification"
      @close="showNotification = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import Mainheader from '../../components/navigator/header.vue'
import collectionWithProducts from '../../components/layout/collectionWithProducts.vue'
import FooterSection from '../../components/layout/footerSection.vue'
import cartModale from '../../components/modale/cartModale.vue'
import notifications from '../../components/tools/notifications.vue'

const isCartOpen = ref<boolean>(false)

const toggleCart = () => {
  isCartOpen.value = !isCartOpen.value
}

const handleProductAdded = () => {
  isCartOpen.value = true
  showNotificationPopup()
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
</script>

<style scoped>
.page-container {
  background-color: #ffffff;
  min-height: 100vh;
}
</style>
