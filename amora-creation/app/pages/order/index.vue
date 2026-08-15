<template>
    <div class="page-container">
        <div class="checkout-wrapper">
            
            <div class="checkout-left">
                <checkoutForm @success="handlePaymentSuccess" />
            </div>

            <div class="checkout-right">
                <summaryCheckout />
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import checkoutForm from '../../components/forms/checkoutForm.vue'
import summaryCheckout from '../../components/tools/summaryCheckout.vue'

/**
 * 💡 Cette fonction est déclenchée SEULEMENT quand le backend a répondu favorablement 
 * à la création de la commande ET à l'initialisation du paiement.
 */
const handlePaymentSuccess = (data: any) => {
    console.log('💳 [Checkout Page] Événement success reçu avec :', data);

    // Si on reçoit bien une URL de la part du backend (la sandbox CinetPay/XPay/Wave, etc.)
    if (data.paymentUrl) {
        console.log('🔗 Redirection en cours vers la plateforme de paiement :', data.paymentUrl);
        // 👉 Redirection de l'utilisateur vers la page de paiement
        window.location.href = data.paymentUrl;
    } 
    // Si la méthode est par carte et que tu gères Stripe dans une modale plus tard (comme ton autre app)
    else if (data.paymentMethod === 'CARD') {
        console.log('🔵 Ouverture éventuelle d\'une modale Stripe (à implémenter si besoin)');
        // isPaiementModale.value = true;
    } 
    else {
        console.error('⚠️ Aucune URL de paiement fournie par le serveur.');
    }
}
</script>

<style scoped>
/* Le fond de la page. Un gris très clair (#f9f9f9) fait mieux ressortir les composants blancs que du blanc pur */
.page-container {
    background-color: #f9f9f9;
    min-height: 100vh;
    width: 100%;
    padding: 40px 20px; /* Espace en haut/bas et sur les côtés */
    display: flex;
    justify-content: center;
    align-items: flex-start; /* Important: pour que le sticky du résumé fonctionne */
}

/* Le conteneur principal (Grille) */
.checkout-wrapper {
    width: 100%;
    max-width: 1100px; /* On limite la largeur sur les très grands écrans */
    display: grid;
    /* Par défaut (sur téléphone), c'est une seule colonne */
    grid-template-columns: 1fr; 
    gap: 40px;
}

.checkout-left {
    width: 100%;
}

.checkout-right {
    width: 100%;
    /* Si on a mis position: sticky dans le composant summaryCheckout, ça marchera ici */
}

/* RESPONSIVE : À partir des tablettes / PC (992px) */
@media (min-width: 992px) {
    .checkout-wrapper {
        /* On passe sur 2 colonnes. 
           1.5fr pour le formulaire (plus large) et 1fr pour le résumé (plus étroit) */
        grid-template-columns: 1.5fr 1fr;
        gap: 60px;
    }
}
</style>