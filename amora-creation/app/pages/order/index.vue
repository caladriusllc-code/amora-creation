<template>
    <div class="page-container">
        <div class="checkout-wrapper">
            
            <div class="checkout-left">
                <checkoutForm @submit-checkout="handleCheckout" />
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

// Cette fonction est déclenchée quand l'utilisateur clique sur "Valider la commande"
const handleCheckout = async (formData: any) => {
    console.log('Prêt à envoyer à Django !', formData)
    
    // C'est ici que tu feras ton appel POST vers ton backend !
    /*
    try {
        const response = await $fetch('http://localhost:8000/order/orders/checkout/', {
            method: 'POST',
            body: {
                ...formData,
                session_key: 'TA_SESSION_KEY_ICI' // À récupérer depuis tes cookies ou ton store
            }
        })
        console.log('Succès !', response)
        // Rediriger vers une page de remerciement
    } catch (error) {
        console.error('Erreur lors du checkout', error)
    }
    */
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