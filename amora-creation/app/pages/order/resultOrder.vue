<template>
  <div class="payment-result-container">
    <div class="status-card">
      
      <div v-if="isLoading" class="state-view loading-state">
        <div class="spinner"></div>
        <h2>Vérification du paiement...</h2>
        <p>Veuillez patienter pendant que nous confirmons votre commande auprès de notre partenaire de paiement.</p>
      </div>

      <div v-else-if="paymentStatus === 'success'" class="state-view success-state">
        <div class="icon-wrapper success-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
        </div>
        <h2>Paiement réussi !</h2>
        <p>Merci pour votre achat chez Amora Création. Votre commande <strong v-if="orderId">#{{ orderId }}</strong> est confirmée.</p>
        <p class="sub-text">Vous recevrez un email de confirmation d'ici quelques minutes.</p>
        
        <button @click="goHome" class="submit-btn">Continuer mes achats</button>
      </div>

      <div v-else class="state-view error-state">
        <div class="icon-wrapper error-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
        </div>
        <h2>Le paiement a échoué</h2>
        <p>Malheureusement, votre paiement a été refusé ou annulé. Aucun montant n'a été débité.</p>
        
        <div class="button-group">
          <button @click="retryPayment" class="submit-btn">Réessayer le paiement</button>
          <button @click="contactSupport" class="outline-btn">Nous contacter</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from '#app'
import { useOrderStore } from '../../stores/orderStore' // Ajuste selon le dossier de ton store
import { useCartStore } from '../../stores/cartStore' // Pour vider le panier en cas de succès

const route = useRoute()
const router = useRouter()
const orderStore = useOrderStore()
const cartStore = useCartStore()

// --- États ---
const isLoading = ref(true)
const paymentStatus = ref<'success' | 'error' | null>(null)
const orderId = ref<string | null>(null)

// N'oublie pas les imports en haut de ton script :
// import { ref, onMounted } from 'vue'
// import { useRoute, useRouter } from '#app'

onMounted(async () => {
  // 1. Récupération des paramètres spécifiques à PaiementPro
  const responseCode = route.query.responsecode as string;
  const returnContextStr = route.query.returnContext as string;
  const referenceNumber = route.query.referenceNumber as string;

  let extractedOrderId = null;

  // 2. Décoder le returnContext (qui est un JSON stringifié dans l'URL)
  if (returnContextStr) {
    try {
      const contextObj = JSON.parse(returnContextStr);
      extractedOrderId = contextObj.order_id;
    } catch (e) {
      console.error("Impossible de lire le returnContext:", e);
    }
  }

  // Assigner l'ID pour l'affichage (priorité à order_id, sinon le numéro de référence du paiement)
  orderId.value = extractedOrderId || referenceNumber || null;

  // Si on n'a pas du tout de code de réponse, on considère que c'est une erreur / page invalide
  if (!responseCode) {
    isLoading.value = false;
    paymentStatus.value = 'error';
    return;
  }

  try {
    // 💡 (Optionnel) Tu pourrais faire un appel API ici pour revérifier le statut réel en base de données.
    await new Promise(resolve => setTimeout(resolve, 1500)); // Petit effet de chargement
    
    // 3. Chez PaiementPro, responsecode == '0' signifie SUCCÈS
    const isSuccess = responseCode === '0';

    if (isSuccess) {
      paymentStatus.value = 'success';
      // Le paiement a réussi : on vide le panier !
      // cartStore.clearCart();
    } else {
      paymentStatus.value = 'error';
    }

  } catch (error) {
    console.error("Erreur lors de la vérification du paiement :", error);
    paymentStatus.value = 'error';
  } finally {
    isLoading.value = false;
  }
})

// --- Actions (Navigation) ---
const goHome = () => {
  router.push('/')
}

const retryPayment = () => {
  router.push('/checkout')
}

const contactSupport = () => {
  router.push('/contact')
}
</script>

<style scoped>
/* Conteneur principal centré */
.payment-result-container {
  min-height: 70vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9f9f9;
  padding: 20px;
}

/* Carte blanche avec ombre */
.status-card {
  background: white;
  width: 100%;
  max-width: 500px;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  text-align: center;
  animation: slideUp 0.5s ease-out;
}

/* Structure commune pour les états */
.state-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.state-view h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.state-view p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.sub-text {
  font-size: 0.9rem;
  color: #999;
}

/* --- Icônes UI --- */
.icon-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
}

.icon-wrapper svg {
  width: 40px;
  height: 40px;
}

.success-icon {
  background-color: #e6f6eb;
  color: #2e7d32;
}

.error-icon {
  background-color: #fdeded;
  color: #d32f2f;
}

/* --- Spinner de Chargement --- */
.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #333; /* Couleur principale Amora */
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

/* --- Boutons --- */
.submit-btn {
  margin-top: 20px;
  width: 100%;
  background-color: #1a1a1a;
  color: #fff;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #333;
}

.button-group {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.outline-btn {
  width: 100%;
  background-color: transparent;
  color: #1a1a1a;
  padding: 14px;
  border: 1px solid #1a1a1a;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.outline-btn:hover {
  background-color: #f5f5f5;
}

/* --- Animations --- */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>