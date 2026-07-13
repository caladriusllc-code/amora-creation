<template>
    <div class="cart-modale-overlay" v-if="isOpen">
        <div class="modale-content">
            <div class="modale-header flex justify-between items-center w-full">
                <h4>Votre panier</h4>
                <button class="close-button" @click="$emit('close')">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <div class="modale-body">
                <h1>Bienvenue dans votre panier</h1>
            </div>

            <div class="modale-footer">

            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    props:{
        isOpen: {
            type: Boolean,
            default: false
        }
    },
    emits: ['close']
}
</script>

<style scoped>
.cart-modale-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000; /* Assure-toi que la modale passe par-dessus tout le reste */
}

.modale-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 1.5rem;
    border-radius: 12px; /* Un petit côté arrondi très chic */
    
    /* Configuration par défaut (Téléphones et Tablettes) */
    width: 90%; /* Laisse une belle petite marge sur les côtés */
    height: 80vh; /* Prend exactement 80% de la hauteur de l'écran */
    overflow-y: auto; /* Ajoute un scroll si tu as beaucoup d'articles dans le panier */

    display: flex;
    flex-direction: column;
    align-items: center;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

/* Configuration Ordinateur (À partir de 992px de large) */
@media (min-width: 992px) {
    .modale-content {
        width: 600px; /* Une largeur fixe élégante pour ordinateur */
        height: auto; /* La hauteur s'adapte au nombre d'articles... */
        max-height: 80vh; /* ...mais ne dépasse jamais 80% de l'écran */
    }
}
</style>