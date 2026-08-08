<template>
    <form @submit.prevent="submitOrder" class="checkout-form">
        <h3>Informations de livraison</h3>
        
        <div class="form-grid">
            <BaseInput 
                v-model="formData.full_name"
                label="Nom complet"
                type="text"
                placeholder="Ex: Awa Diallo"
                required
            />

            <BaseInput 
                v-model="formData.email"
                label="Adresse Email"
                type="email"
                placeholder="cliente.amora@example.com"
                required
            />

            <BaseInput 
                v-model="formData.phone_number"
                label="Numéro de téléphone"
                type="tel"
                placeholder="Ex: +225 01 02 03 04 05"
                required
            />

            <BaseInput 
                v-model="formData.city"
                label="Ville"
                type="text"
                placeholder="Ex: Abidjan"
                required
            />

            <div class="full-width">
                <BaseInput 
                    v-model="formData.shipping_address"
                    label="Adresse complète"
                    type="text"
                    placeholder="Ex: Cocody Angré, Rue des Jardins"
                    required
                />
            </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
            {{ isLoading ? 'Validation en cours...' : 'Valider la commande' }}
        </button>
    </form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
// L'import de BaseInput n'est pas strictement nécessaire dans Nuxt 3 
import BaseInput from '../input/BaseInput.vue' 
import {useOrderStore} from '../../stores/orderStore'
import type {Order} from '../../stores/orderStore'

const orderStore = useOrderStore();

// État de chargement pour le bouton
const isLoading = ref(false)

// Données du formulaire liées aux BaseInput via v-model
const formData = ref<Order>({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: ''
})

// Définition de l'événement qu'on va envoyer au composant parent (la page Checkout)
const emit = defineEmits(['submit-checkout'])

const submitOrder = async () => {
    isLoading.value = true
    
    try {
        orderStore.checkout(formData.value);
        emit('submit-checkout', formData.value)
    } finally {
        // Dans la vraie vie, le parent gérera la fin du chargement après l'appel API
        isLoading.value = false
    }
}
</script>

<style scoped>
.checkout-form {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

h3 {
    margin-bottom: 24px;
    color: #333;
    font-size: 1.5rem;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 24px;
}

/* Sur mobile, on passe tout sur une seule colonne */
@media (max-width: 768px) {
    .form-grid {
        grid-template-columns: 1fr;
    }
}

.full-width {
    grid-column: 1 / -1;
}

.submit-btn {
    width: 100%;
    padding: 14px;
    background-color: #000; /* À adapter avec les couleurs Amora */
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.submit-btn:hover {
    background-color: #333;
}

.submit-btn:disabled {
    background-color: #ccc;
    cursor: not-allowed;
}
</style>