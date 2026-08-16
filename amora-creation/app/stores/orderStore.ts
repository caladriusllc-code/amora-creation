import { defineStore } from "pinia";
import { ref } from "vue";
import { useNuxtApp } from "#app";
import type { Message } from './cartStore'

export interface GuestInfo {
    id?: string;
    email: string;
    full_name: string;
    phone_number: string;
    shipping_address: string;
    city?: string;
    created_at?: string;
}

export interface Order {
    id?: string;
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

export interface Paiement {
    amount: number;
    channel: string;
    referenceNumber: string;
    customerEmail: string;
    customerFirstName: string;
    customerLastname: string;
    customerPhoneNumber: string;
    description: string;
    merchantId?: string;
    notificationURL?: string;
    returnURL?: string;
    returnContext?: string;
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
    
    // Dans ton store (useOrderStore)
    async function checkout(payload: GuestInfo) {
        isLoading.value = true;

        try {
            const response: any = await $api('order/orders/checkout/', {
                method: 'POST',
                body: payload
            });

            if(response) {
                console.log("Votre commande a été bien enrégistrée", response);

                const normalizedResponse: any = {
                    ...response,
                    id: response.id ?? response.order_id ?? response.order?.id,
                    order_id: response.order_id ?? response.id ?? response.order?.id,
                };

                order.value = normalizedResponse as unknown as Order;
                return normalizedResponse;
            }
        } catch(error: any) {
            console.error("Erreur de soumission de votre commande:", error);
            // C'est une bonne pratique de propager l'erreur pour que le composant puisse l'attraper
            throw error; 
        } finally {
            isLoading.value = false;
        }
    }

    async function initiatePayment(payload?: any, email?: string){

        isLoading.value = true;
        
        try{
            const emailQuery = email ? `?email=${encodeURIComponent(email)}` : '';
            const bodyData = payload ? payload : {};

            const response = await $api(`/payment/initiate/${emailQuery}`, {
                method: 'POST',
                body: bodyData
            });

            return response;
        } catch (err: any) {
        message.value = err.message;
        throw err;
        } finally {
        isLoading.value = false;
        }

    }

    return {
        isLoading,
        message,
        order,
        checkout,
        initiatePayment
    }
})