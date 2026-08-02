<template>
  <button class="cart-button" :disabled="isButtonLoading" :aria-busy="isButtonLoading">
    <svg 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" viewBox="0 0 24 24" 
        stroke-width="1.5" 
        stroke="currentColor" class="size-6"
        v-if="!isButtonLoading"
    >
        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
    </svg>
    
    <span class="loading loading-spinner loading-md" v-else></span>

    <span v-if="badgeCount && badgeCount > 0" class="cart-badge">
      {{ badgeCount > 99 ? '99+' : badgeCount }}
    </span>
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  isLoading?: boolean;
  loading?: boolean;
  badgeCount?: number; // ✨ Nouvelle propriété pour le badge
}>(), {
  isLoading: false,
  loading: false,
  badgeCount: 0,       // Par défaut à 0 (donc invisible)
});

const isButtonLoading = computed(() => props.isLoading || props.loading);
</script>

<style scoped>
.cart-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 4px;
    background-color: #000;
    color: #fff;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    
    /* ✨ IMPORTANT : Permet de positionner le badge de manière absolue par rapport au bouton */
    position: relative; 
}

/* =========================================
   🔴 STYLES DU BADGE
   ========================================= */
.cart-badge {
    position: absolute;
    top: -6px;
    right: -6px;
    background-color: #ef4444; /* Rouge vif pour capter l'attention */
    color: white;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Urbanist', sans-serif;
    
    /* Dimensions pour faire un cercle parfait */
    height: 20px;
    min-width: 20px;
    padding: 0 5px;
    border-radius: 10px;
    
    /* Centrage du texte */
    display: flex;
    align-items: center;
    justify-content: center;
    
    /* Ombre légère pour détacher le badge */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    
    /* Petite animation sympa quand le badge apparaît */
    animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes popIn {
    0% { transform: scale(0); }
    100% { transform: scale(1); }
}
</style>