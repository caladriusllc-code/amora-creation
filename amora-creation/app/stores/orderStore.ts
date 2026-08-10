import { defineStore } from "pinia";
import { ref } from "vue";
import { useNuxtApp } from "#app";
import type { Message } from './cartStore'

export interface GuestInfo {
    id?: string;
    email: string;
    full_name: string;
    phone_number?: string | null;
    shipping_address: string;
    city?: string;
    created_at?: string;
}

export interface Order {
    id: string;
    guest?: GuestInfo | null;
    status?: string;
    total_amount: number;
    created_at?: string;
}

export interface OrderItem {
    id: string;
    order_id?: string;
    contrat?: any;
    unit_price?: number;
    quantity?: number;
    created_at?: string;
}

export const useOrderStore = defineStore('order', () => {

    const { $api } = useNuxtApp();

    // Ux
    const isLoading = ref<boolean>(false);
    const message = ref<Message | null>(null)

    // State
    const order = ref<Order | null>(null);

    // Actions
    // 💡 CORRECTION ICI : Le payload est de type GuestInfo, car c'est ce que le formulaire envoie
    async function checkout(payload: GuestInfo) {
        isLoading.value = true;

        try {
            const response = await $api('order/orders/checkout/', {
                method: 'POST',
                body: payload
            });

            if(response) {
                console.log("Votre commande a été bien enrégistrée", response);
                // Si l'API retourne la commande créée, tu peux l'assigner :
                // order.value = response
            }
        } catch(error: any) {
            console.error("Erreur de soumission de votre commande:", error);
        } finally {
            isLoading.value = false;
        }
    }

    return {
        isLoading,
        message,
        order,
        checkout
    }
})