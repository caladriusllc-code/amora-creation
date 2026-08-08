import {defineStore} from "pinia";
import {ref, computed} from "vue";
import {useNuxtApp} from "#app";

import type {Message} from './cartStore'

export interface Order{

    session_key?: string,
    email: string,
    full_name: string,
    phone_number: string,
    shipping_address: string
    city: string

}

export const useOrderStore = defineStore('order', ()=>{

    const {$api} = useNuxtApp();

    // Ux
    const isLoading = ref<boolean>(false);
    const message = ref<Message | null>(null)

    // State
    const order = ref<Order | null>(null);

    //Guetters

    // Actions
    async function checkout(payload:Order){

        isLoading.value = true;

        try{
            const response = await $api('order/orders/checkout/', {
                method: 'POST',
                body: payload
            });

            if(response){

                console.log("Votre commande a été bien enrégistré", response);
            }
        } catch(error: any){
            console.error("Erreur de soumission de votre commande:", error);
        } finally{
            isLoading.value = false;
        }
    }

    return{
        isLoading,
        message,
        order,
        checkout
    }



})