<template>
    <form @submit.prevent="submitOrder" class="checkout-form">
        <h3>Informations de livraison</h3>
        
        <div class="form-grid">
            <BaseInput 
                v-model="formData.full_name"
                label="Nom complet"
                type="text"
                placeholder="Ex: Awa Diallo"
                :errorMessage="errors.full_name"
                @input="clearError('full_name')"
            />

            <BaseInput 
                v-model="formData.email"
                label="Adresse Email"
                type="email"
                placeholder="cliente.amora@example.com"
                :errorMessage="errors.email"
                @input="clearError('email')"
            />

            <BaseInput 
                v-model="formData.phone_number"
                label="Numéro de téléphone"
                type="tel"
                placeholder="Ex: +225 01 02 03 04 05"
                :errorMessage="errors.phone_number"
                @input="clearError('phone_number')"
            />

            <BaseInput 
                v-model="formData.city"
                label="Ville"
                type="text"
                placeholder="Ex: Abidjan"
                :errorMessage="errors.city"
                @input="clearError('city')"
            />

            <div class="full-width">
                <BaseInput 
                    v-model="formData.shipping_address"
                    label="Adresse complète"
                    type="text"
                    placeholder="Ex: Cocody Angré, Rue des Jardins"
                    :errorMessage="errors.shipping_address"
                    @input="clearError('shipping_address')"
                />
            </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
            {{ isLoading ? 'Validation en cours...' : 'Valider la commande' }}
        </button>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseInput from '../input/BaseInput.vue' 
import { useOrderStore } from '../../stores/orderStore'
import type { Order } from '../../stores/orderStore'

const orderStore = useOrderStore();
const emit = defineEmits(['submit-checkout'])

// État de chargement
const isLoading = ref(false)

// Données du formulaire
const formData = ref<Order>({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: ''
})

// État des erreurs pour le nouveau composant BaseInput
const errors = ref({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: ''
})

// Fonction pour effacer l'erreur dès que l'utilisateur commence à taper
const clearError = (field: keyof typeof errors.value) => {
    errors.value[field] = ''
}

// Fonction de validation du formulaire
const validateForm = () => {
    let isValid = true;
    
    // Réinitialiser les erreurs
    Object.keys(errors.value).forEach(key => {
        errors.value[key as keyof typeof errors.value] = ''
    });

    if (!formData.value.full_name.trim()) {
        errors.value.full_name = 'Le nom est requis.';
        isValid = false;
    }

    if (!formData.value.email.trim()) {
        errors.value.email = 'L\'email est requis.';
        isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
        errors.value.email = 'Veuillez entrer un email valide.';
        isValid = false;
    }

    if (!formData.value.phone_number.trim()) {
        errors.value.phone_number = 'Le numéro de téléphone est requis.';
        isValid = false;
    }

    if (!formData.value.city.trim()) {
        errors.value.city = 'La ville est requise.';
        isValid = false;
    }

    if (!formData.value.shipping_address.trim()) {
        errors.value.shipping_address = 'L\'adresse complète est requise.';
        isValid = false;
    }

    return isValid;
}

const submitOrder = async () => {
    // 1. On valide d'abord le formulaire (ce qui va afficher les messages d'erreur si besoin)
    if (!validateForm()) {
        return; // On stop ici si c'est invalide
    }

    // 2. Si c'est valide, on lance la requête
    isLoading.value = true
    
    try {
        await orderStore.checkout(formData.value);
        emit('submit-checkout', formData.value)
    } catch (error) {
        console.error("Erreur lors de la validation de la commande", error);
        // Ici tu pourrais gérer les erreurs retournées par Django (ex: stock insuffisant)
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
/* Le CSS reste identique, la magie opère via les composants enfants ! */
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
    background-color: #000;
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