<template>
    <div class="page-container">
        <div class="checkout-wrapper">
            
            <div class="checkout-left">
                <!-- ⚡️ Écoute de l'événement de mise à jour des frais -->
                <checkoutForm @success="handlePaymentSuccess" @shipping-updated="updateShippingFee" />
            </div>

            <div class="checkout-right">
                <!-- ⚡️ Transmission des frais au résumé -->
                <summaryCheckout :shippingFee="shippingFee" />
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import checkoutForm from '../../components/forms/checkoutForm.vue'
import summaryCheckout from '../../components/tools/summaryCheckout.vue'

// ⚡️ État pour stocker les frais de livraison
const shippingFee = ref<number>(0);

const updateShippingFee = (fee: number) => {
    shippingFee.value = fee;
};

/**
 * 💡 Cette fonction est déclenchée SEULEMENT quand le backend a répondu favorablement 
 * à la création de la commande ET à l'initialisation du paiement.
 */
const handlePaymentSuccess = (data: any) => {
    console.log('💳 [Checkout Page] Événement success reçu avec :', data);

    if (data.paymentUrl) {
        console.log('🔗 Redirection en cours vers la plateforme de paiement :', data.paymentUrl);
        window.location.href = data.paymentUrl;
    } 
    else if (data.paymentMethod === 'CARD') {
        console.log('🔵 Ouverture éventuelle d\'une modale Stripe (à implémenter si besoin)');
    } 
    else {
        console.error('⚠️ Aucune URL de paiement fournie par le serveur.');
    }
}
</script>

<style scoped>
/* Le CSS reste inchangé par rapport à ton code d'origine */
.page-container {
    background-color: #f9f9f9;
    min-height: 100vh;
    width: 100%;
    padding: 40px 20px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
}

.checkout-wrapper {
    width: 100%;
    max-width: 1100px;
    display: grid;
    grid-template-columns: 1fr; 
    gap: 40px;
}

.checkout-left {
    width: 100%;
}

.checkout-right {
    width: 100%;
}

@media (min-width: 992px) {
    .checkout-wrapper {
        grid-template-columns: 1.5fr 1fr;
        gap: 60px;
    }
}
</style>