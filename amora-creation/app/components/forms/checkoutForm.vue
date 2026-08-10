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

            <BaseSelect 
                v-model="formData.city"
                :options="cityOptions"
                placeholder="Moyen de paiement"
                :errorMessage="errors.city"
            />
        </div>

        <button type="submit" class="submit-btn" :disabled="orderStore.isLoading">
            {{ orderStore.isLoading ? 'Validation en cours...' : 'Valider la commande' }}
        </button>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseInput from '../input/BaseInput.vue' 
import BaseSelect from '../input/BaseSelect.vue'
import { useOrderStore } from '../../stores/orderStore'
import type { GuestInfo } from '../../stores/orderStore'

const orderStore = useOrderStore();
const emit = defineEmits(['submit-checkout'])

// 💡 SUPPRIMÉ : const isLoading = ref(false) (On utilise celui du store)

const formData = ref<GuestInfo>({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: ''
})

const errors = ref({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: ''
})

const clearError = (field: keyof typeof errors.value) => {
    errors.value[field] = ''
}

// Le format attendu par ton composant BaseSelect
const cityOptions = ref([
  { label: 'Abidjan', value: 'abidjan' },
  { label: 'Yamoussoukro', value: 'yamoussoukro' },
  { label: 'Bouaké', value: 'bouake' }
]);

const validateForm = () => {
    let isValid = true;
    
    Object.keys(errors.value).forEach(key => {
        errors.value[key as keyof typeof errors.value] = ''
    });

    // 💡 CORRECTION ICI : On sécurise le .trim() au cas où la valeur serait null ou undefined
    if (!(formData.value.full_name || '').trim()) {
        errors.value.full_name = 'Le nom est requis.';
        isValid = false;
    }

    if (!(formData.value.email || '').trim()) {
        errors.value.email = 'L\'email est requis.';
        isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
        errors.value.email = 'Veuillez entrer un email valide.';
        isValid = false;
    }

    if (!(formData.value.phone_number || '').trim()) {
        errors.value.phone_number = 'Le numéro de téléphone est requis.';
        isValid = false;
    }

    if (!(formData.value.city || '').trim()) {
        errors.value.city = 'La ville est requise.';
        isValid = false;
    }

    if (!(formData.value.shipping_address || '').trim()) {
        errors.value.shipping_address = 'L\'adresse complète est requise.';
        isValid = false;
    }

    return isValid;
}

const submitOrder = async () => {
    if (!validateForm()) {
        return; 
    }
    
    try {
        // 💡 Le store gère maintenant lui-même son orderStore.isLoading = true / false
        await orderStore.checkout(formData.value);
        emit('submit-checkout', formData.value)
    } catch (error) {
        console.error("Erreur lors de la validation de la commande", error);
    }
}
</script>

<style scoped>
/* Ton CSS original reste inchangé, il est parfait ! */
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