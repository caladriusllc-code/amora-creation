<template>
  <Transition name="slide-fade">
    <div v-if="isVisible" class="notification-popup">
      <div class="unread-indicator"></div>
      
      <div class="notif-icon-container">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2D4B46" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
          <circle cx="8.5" cy="7" r="4"></circle>
          <polyline points="17 11 19 13 23 9"></polyline>
        </svg>
      </div>

      <div class="notif-content">
        <p class="notif-text">
          {{ actionText }} <strong>{{ userName }}</strong>
        </p>
        <span class="notif-time">{{ time }}</span>
      </div>

      <button class="close-btn" @click="closePopup" aria-label="Fermer">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  </Transition>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';

export default {
    name: 'NotificationPopup',
    props:{
        userName: {
            type: String,
            default: 'Olamina'
        },
        actionText: {
            type: String,
            default: 'Un nouveau contrat a été créé par'
        },
        time: {
            type: String,
            default: 'à l\'instant'
        },
        duration: {
            type: Number,
            default: 20000 // Disparaît après 5 secondes (mettre 0 pour la garder indéfiniment)
        }
    },

    emits: ['close'],
    setup(props, {emit}){

        const isVisible = ref(true);

        const closePopup = () => {
        isVisible.value = false;
        // On prévient le composant parent qu'elle est fermée
        setTimeout(() => emit('close'), 300); 
        };

        // Fermeture automatique
        onMounted(() => {
            if (props.duration > 0) {
                setTimeout(() => {
                //closePopup();
                }, props.duration);
            }
        });

        return {
            isVisible,
            closePopup
        }
    }
}

// On définit les propriétés pour pouvoir afficher des messages dynamiques



</script>

<style scoped>
/* Conteneur principal de la popup */
.notification-popup {
  position: fixed;
  top: 24px;
  right: 24px;
  width: 380px;
  max-width: calc(100vw - 48px);
  background-color: #2D4B46; /* Vert foncé de ton image */
  border: 1px solid #3A5F59;
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
  z-index: 9999;
  font-family: sans-serif;
}

/* Le petit point bleu */
.unread-indicator {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  background-color: #3B82F6;
  border-radius: 50%;
}

/* Conteneur de l'icône */
.notif-icon-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #26423E;
  border: 1px solid #3A5F59;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-left: 8px; /* Espace pour le point bleu */
}

/* Textes */
.notif-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.notif-text {
  font-size: 14px;
  color: #E5E7EB;
  margin: 0;
  line-height: 1.4;
}

.notif-text strong {
  font-weight: 600;
  color: #FFFFFF;
}

.notif-time {
  font-size: 12px;
  color: #9CA3AF;
}

/* Bouton fermer (la petite croix) */
.close-btn {
  background: none;
  border: none;
  color: #9CA3AF;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  color: #FFFFFF;
  background-color: #3A635E;
}

/* Animations d'apparition et disparition */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(50px);
  opacity: 0;
}
</style>