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

            <!-- ⚡️ NOUVEAU : Sélection de la zone de livraison -->
            <div class="full-width">
                <p v-if="shippingZonesLoading" class="shipping-status">Chargement des zones de livraison...</p>
                <p v-else-if="shippingZones.length === 0" class="shipping-status shipping-status-empty">Aucune zone de livraison disponible.</p>
                <BaseSelect
                    v-else
                    v-model="formData.shipping_zone"
                    label="Zone de livraison"
                    :options="shippingZones"
                    placeholder="Sélectionnez votre zone de livraison"
                    :errorMessage="errors.shipping_zone"
                    @change="handleShippingChange"
                />
            </div>

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

            <div class="full-width">
                <BaseCheckboxe
                    v-model="formData.accept_cgv"
                    :errorMessage="errors.accept_cgv"
                    @change="clearError('accept_cgv')"
                />
            </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="orderStore.isLoading || cartStore.isLoading">
            {{ (orderStore.isLoading || cartStore.isLoading) ? 'Traitement en cours...' : 'Valider et Payer' }}
        </button>
    </form>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import BaseInput from '../input/BaseInput.vue'
import BaseSelect from '../input/BaseSelect.vue'
import BaseCheckboxe from '../input/BaseCheckboxe.vue'
import { useCookie, useNuxtApp } from '#app'

import { useOrderStore } from '../../stores/orderStore'
import { useCartStore } from '../../stores/cartStore'
import type { GuestInfo } from '../../stores/orderStore'

interface ShippingRate {
    min_weight: string
    max_weight: string
    price: string
}

interface ShippingZoneResponse {
    id: number
    name: string
    rates: ShippingRate[]
    shipping_fee: string
}

const orderStore = useOrderStore();
const cartStore = useCartStore();

// ⚡️ Ajout de 'shipping-updated' pour émettre le montant des frais au composant parent
const emit = defineEmits(['success', 'submit-checkout', 'shipping-updated'])

const notify = ref({ show: false, type: 'success', title: '', message: '' });
const showNotification = (type: 'success' | 'error', title: string, message = '') => {
    notify.value = { show: true, type, title, message };
};

// ⚡️ Ajout de shipping_zone au formulaire et aux erreurs
const formData = ref<GuestInfo & { payment_method: string, accept_cgv: boolean, shipping_zone: string }>({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: '',
    payment_method: '',
    shipping_zone: '',
    accept_cgv: false
})

const errors = ref({
    full_name: '',
    email: '',
    phone_number: '',
    city: '',
    shipping_address: '',
    payment_method: '',
    shipping_zone: '',
    accept_cgv: ''
})

const clearError = (field: keyof typeof errors.value) => {
    errors.value[field] = ''
}

const { $api } = useNuxtApp();
const shippingZonesLoading = ref(false);
const shippingZones = ref<Array<{ value: number, name: string, label: string, fee: number, rates: ShippingRate[] }>>([]);

const formatPrice = (value: number) => `${value.toLocaleString('fr-FR')} FCFA`;

const fetchShippingZones = async () => {
    shippingZonesLoading.value = true;
    try {
        const response = await $api<{ zones: ShippingZoneResponse[] }>('/order/orders/shipping-zones/');
        shippingZones.value = (response.zones || []).map(zone => ({
            value: zone.id,
            name: zone.name,
            fee: Number(zone.shipping_fee) || 0,
            rates: zone.rates || [],
            label: `${zone.name}${Number(zone.shipping_fee) > 0 ? ` - ${formatPrice(Number(zone.shipping_fee))}` : ''}`
        }));
    } catch (error) {
        console.error('Erreur lors du chargement des zones de livraison:', error);
        shippingZones.value = [];
    } finally {
        shippingZonesLoading.value = false;
    }
};

onMounted(async () => {
    if (!cartStore.cart) {
        await cartStore.fetchCart();
    }
    await fetchShippingZones();
});

// ⚡️ NOUVEAU : Fonction qui cherche le montant lié à la zone et l'émet au parent
const handleShippingChange = () => {
    clearError('shipping_zone');
    const selectedZone = shippingZones.value.find(zone => zone.value === Number(formData.value.shipping_zone));
    const fee = selectedZone ? selectedZone.fee : 0;
    emit('shipping-updated', fee);
};

const paymentOptions = ref([
    { value: 'WAVE',         name: 'Wave',          label: 'Wave' },
    { value: 'OMCIV2',       name: 'Orange Money',  label: 'Orange Money' },
    { value: 'FLOOZ',        name: 'Moov Money',    label: 'Moov Money' },
    { value: 'CARD',         name: 'Visa/MasterCard', label: 'Visa/MasterCard'}
]);

const validateForm = () => {
    let isValid = true;
    Object.keys(errors.value).forEach(key => { errors.value[key as keyof typeof errors.value] = '' });

    if (!(formData.value.full_name || '').trim()) { errors.value.full_name = 'Le nom est requis.'; isValid = false; }
    if (!(formData.value.email || '').trim()) { errors.value.email = 'L\'email est requis.'; isValid = false; } 
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) { errors.value.email = 'Veuillez entrer un email valide.'; isValid = false; }
    if (!(formData.value.phone_number || '').trim()) { errors.value.phone_number = 'Le numéro de téléphone est requis.'; isValid = false; }
    if (!(formData.value.city || '').trim()) { errors.value.city = 'La ville est requise.'; isValid = false; }
    
    // ⚡️ Validation de la zone de livraison
    if (!formData.value.shipping_zone) { errors.value.shipping_zone = 'Veuillez choisir une zone de livraison.'; isValid = false; }
    
    if (!(formData.value.shipping_address || '').trim()) { errors.value.shipping_address = 'L\'adresse complète est requise.'; isValid = false; }
    if (!formData.value.payment_method) { errors.value.payment_method = 'Veuillez choisir un moyen de paiement.'; isValid = false; }
    if (!formData.value.accept_cgv) { errors.value.accept_cgv = 'Vous devez accepter les conditions générales de vente pour continuer.'; isValid = false; }

    return isValid;
}

const submitOrder = async () => {
    if (!validateForm()) {
        showNotification('error', 'Champs manquants', 'Veuillez corriger les erreurs sur le formulaire.');
        return;
    }

    const backupEmailCookie = useCookie('backup_checkout_email', { maxAge: 3600 });
    backupEmailCookie.value = formData.value.email;

    try {
        const payloadGuest: any = {
            full_name: formData.value.full_name,
            email: formData.value.email,
            phone_number: formData.value.phone_number,
            city: formData.value.city,
            shipping_address: formData.value.shipping_address,
            // ⚡️ On envoie la zone au backend
            shipping_zone: formData.value.shipping_zone 
        };

        const order: any = await orderStore.checkout(payloadGuest);
        const orderId = order?.id ?? order?.order_id;

        if (!orderId) { showNotification('error', 'Erreur système', "Impossible de générer l'identifiant de la commande."); return; }

        const paiementResponse: any = await orderStore.initiatePayment({ order_id: orderId, payment_method: formData.value.payment_method.toUpperCase() }, formData.value.email);
        const paymentUrl = paiementResponse?.payment_url || paiementResponse?.data?.payment_url || null;

        emit('success', { paymentMethod: formData.value.payment_method, email: formData.value.email, fullName: formData.value.full_name, phone: formData.value.phone_number, paymentUrl });
        emit('submit-checkout', formData.value);

    } catch (error: any) {
        console.error("Erreur lors de la validation :", error);
        const errorMsg = error?.response?._data?.error || error?.response?._data?.message || error?.message || "Une erreur est survenue lors de l'initialisation du paiement.";
        showNotification('error', 'Échec de la commande', errorMsg);
    }
}

watch(
    () => [formData.value.shipping_zone, cartStore.cart?.total_weight], 
    ([newZoneId, totalWeight]) => {
        if (!newZoneId) return;
        clearError('shipping_zone');
        
        const selectedZone = shippingZones.value.find(zone => zone.value === Number(newZoneId));
        if (!selectedZone) return;

        // On part sur le tarif de base par défaut
        let fee = selectedZone.fee; 
        const cartWeight = Number(totalWeight) || 0;

        // ⚡️ NOUVEAU : On cherche la bonne tranche de poids dans la grille tarifaire
        if (selectedZone.rates && selectedZone.rates.length > 0) {
            const applicableRate = selectedZone.rates.find(rate => {
                const min = Number(rate.min_weight);
                const max = Number(rate.max_weight);
                return cartWeight >= min && cartWeight <= max;
            });

            if (applicableRate) {
                fee = Number(applicableRate.price);
            }
        }
        
        emit('shipping-updated', fee);
    }
);
</script>

<style scoped>
/* Les styles restent identiques à l'original */
.checkout-form { width: 100%; max-width: 600px; margin: 0 auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
h3 { margin-bottom: 24px; color: #333; font-size: 1.5rem; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }
@media (max-width: 768px) { .form-grid { grid-template-columns: 1fr; } }
.full-width { grid-column: 1 / -1; }
.submit-btn { width: 100%; padding: 14px; background-color: #000; color: #fff; border: none; border-radius: 4px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: background-color 0.3s ease; }
.submit-btn:hover { background-color: #333; }
.submit-btn:disabled { background-color: #ccc; cursor: not-allowed; }
</style>