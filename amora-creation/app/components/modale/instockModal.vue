<template>
  <Transition name="fade">
    <div v-if="isOpen" class="modal-overlay blurred-overlay" @click.self="$emit('close')">
      <div class="modal-content">
        <button class="close-button" @click="$emit('close')" aria-label="Fermer">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div class="icon-wrapper">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="alert-icon">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15.182 15.182a4.5 4.5 0 0 1-6.364 0M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0ZM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75Zm-.375 0h.008v.015h-.008V9.75Z" />
          </svg>
        </div>
        
        <h3 class="modal-title">Rupture de stock</h3>
        
        <p class="modal-text">
          Le produit <strong v-if="productName">{{ productName }}</strong> est malheureusement victime de son succès et n'est plus disponible dans cette configuration.
        </p>
        
        <button class="action-btn" @click="$emit('close')">
          Continuer mes achats
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
defineProps<{
  isOpen: boolean;
  productName?: string;
}>();

defineEmits(['close']);
</script>

<style scoped>
/* =========================================
   OVERLAY FLOU
   ========================================= */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  /* L'astuce du flou réside ici : background semi-transparent + backdrop-filter */
  background-color: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

/* =========================================
   CONTENU DE LA MODALE
   ========================================= */
.modal-content {
  position: relative;
  background-color: #ffffff;
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
  padding: 2.5rem 2rem;
  text-align: center;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #111827;
}

.close-button svg {
  width: 20px;
  height: 20px;
}

/* =========================================
   ICÔNE & TEXTE
   ========================================= */
.icon-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.alert-icon {
  width: 56px;
  height: 56px;
  color: #6b7280;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
}

.modal-text {
  font-size: 1rem;
  color: #4b5563;
  line-height: 1.5;
  margin-bottom: 2rem;
}

/* =========================================
   BOUTON D'ACTION
   ========================================= */
.action-btn {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background-color: #111827;
  color: #ffffff;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.action-btn:hover {
  background-color: #374151;
}

/* =========================================
   TRANSITIONS (Similaire à cartModale)
   ========================================= */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-active .modal-content {
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.fade-enter-from .modal-content {
  transform: scale(0.95) translateY(10px);
}
</style>