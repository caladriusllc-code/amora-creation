<template>
    <form @submit.prevent="submitOrder" class="checkout-form">
        <h3>Informations de livraison et paiement</h3>
        
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

            <div class="full-width">
                <BaseSelect 
                    v-model="formData.payment_method"
                    label="Sélectionner votre moyen de paiement"
                    :options="paymentOptions"
                    placeholder="Choisissez un moyen de paiement"
                    :errorMessage="errors.payment_method"
                    @change="clearError('payment_method')"
                />
            </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="orderStore.isLoading || cartStore.isLoading">
            {{ (orderStore.isLoading || cartStore.isLoading) ? 'Traitement en cours...' : 'Valider et Payer' }}
        </button>
    </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseInput from '../input/BaseInput.vue' 
import BaseSelect from '../input/BaseSelect.vue'
import { useCookie } from '#app'

import { useOrderStore } from '../../stores/orderStore'
import { useCartStore } from '../../stores/cartStore' // 👈 Import du store gérant le paiement
import type { GuestInfo } from '../../stores/orderStore'

const orderStore = useOrderStore();
const cartStore = useCartStore(); 
const emit = defineEmits(['success', 'submit-checkout'])

// ── État de la notification ───────────────────────────────────────
const notify = ref({
    show: false,
    type: 'success',
    title: '',
    message: ''
});

const showNotification = (type: 'success' | 'error', title: string, message = '') => {
    notify.value = { show: true, type, title, message };
};

// ── État du formulaire étendu (GuestInfo + payment_method) ────────
const formData = ref<GuestInfo & { payment_method: string }>({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: '',
    payment_method: '' // 👈 Ajout du mode de paiement
})

const errors = ref({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: '',
    payment_method: ''
})

const clearError = (field: keyof typeof errors.value) => {
    errors.value[field] = ''
}

// ── Options de paiement (mix des deux applications) ───────────────
const paymentOptions = ref([
    { value: 'WAVE',         name: 'Wave',          label: 'Wave' },
    { value: 'OMCIV2',       name: 'Orange Money',  label: 'Orange Money' },
    { value: 'FLOOZ',        name: 'Moov Money',    label: 'Moov Money' },
    { value: 'CARD',         name: 'Visa/MasterCard', label: 'Visa/MasterCard'}
    // Ajoute les autres options si besoin...
]);

// ── Validation ────────────────────────────────────────────────────
const validateForm = () => {
    let isValid = true;
    
    Object.keys(errors.value).forEach(key => {
        errors.value[key as keyof typeof errors.value] = ''
    });

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

    if (!formData.value.payment_method) {
        errors.value.payment_method = 'Veuillez choisir un moyen de paiement.';
        isValid = false;
    }

    return isValid;
}

// ── Soumission globale ────────────────────────────────────────────
const submitOrder = async () => {
    if (!validateForm()) {
        showNotification('error', 'Champs manquants', 'Veuillez corriger les erreurs sur le formulaire.');
        return; 
    }

    // 🔥 Sécurisation de l'email avec le composable Nuxt 3 useCookie
    const backupEmailCookie = useCookie('backup_checkout_email', { maxAge: 3600 });
    backupEmailCookie.value = formData.value.email;
    
    try {
        // 1. On sépare les données client (GuestInfo) du moyen de paiement
        const payloadGuest: GuestInfo = {
            full_name: formData.value.full_name,
            email: formData.value.email,
            phone_number: formData.value.phone_number,
            city: formData.value.city,
            shipping_address: formData.value.shipping_address
        };

        // 2. On crée la commande dans le backend
        const order: any = await orderStore.checkout(payloadGuest);
        const orderId = order?.id ?? order?.order_id;

        // Sécurité : On s'assure que la commande a bien été générée
        if (!orderId) {
            showNotification('error', 'Erreur système', "Impossible de générer l'identifiant de la commande.");
            return;
        }

        // 3. On initialise le paiement avec l'ID de la nouvelle commande
        const paiementResponse: any = await orderStore.initiatePayment(
            {
                order_id: orderId,
                payment_method: formData.value.payment_method.toUpperCase()
            },
            formData.value.email
        );

        const paymentUrl = paiementResponse?.payment_url || paiementResponse?.data?.payment_url || null;

        // 4. On remonte l'événement vers la vue parente pour éventuellement faire une redirection
        emit('success', {
            paymentMethod: formData.value.payment_method,
            email: formData.value.email,
            fullName: formData.value.full_name,
            phone: formData.value.phone_number,
            paymentUrl,
        });
        
        emit('submit-checkout', formData.value);

    } catch (error: any) {
        console.error("Erreur lors de la validation :", error);
        const errorMsg = error?.response?._data?.message
            || error?.message
            || "Une erreur est survenue lors de l'initialisation du paiement.";
        showNotification('error', 'Échec de la commande', errorMsg);
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