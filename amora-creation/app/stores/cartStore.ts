import {defineStore} from "pinia";
import {ref, computed} from "vue";
import {useNuxtApp} from "#app";

import type {Product, Size, Color} from './productStore'

export interface Message {
    success: string,
    fail: string
}

export interface CartItem {
    id: number | string,
    product: Product,
    quantity: number,
    size?: Size,
    color?: Color,
}

export interface Cart {
    id: string,
    session_id: string,
    items: Array<CartItem>,
    coupon?: string,
    total: number,
    total_with_discount?: number
}

export const useCartStore = defineStore('cart', () => {

    const {$api} = useNuxtApp();

    // Ux
    const isLoading = ref<boolean>(false);
    const message = ref<Message | null>(null)

    // State
    const cart = ref<Cart | null>(null);

    // Getters
    const totalItems = computed(()=> {
        if(cart.value && cart.value.items){
            return cart.value.items.reduce((acc, item) => acc + item.quantity, 0);
        }
        return 0;
    })

    // Actions
    async function fetchCart(){

        isLoading.value = true;
        message.value = null;

        try {
            const response = await $api('/cart/cart/get_cart/',{
                method: 'GET'
            })

            if (response) {
                cart.value = response;
            }
        } catch (error: Error | any) {
            console.error("Erreur fetchCart:", error);
        } finally {
            isLoading.value = false;
        }

    }

    async function addToCart(productId: string | number, quantity: number = 1, sizeId?: number, colorId?: number){
        isLoading.value = true;
        message.value = null;

        try {
            const body: any = {
                product_id: productId,
                quantity: quantity
            };

            // Ajouter la taille et la couleur si elles sont fournies
            if (sizeId) body.size_id = sizeId;
            if (colorId) body.color_id = colorId;

            const response = await $api('/cart/cart/add_item/',{
                method: 'POST',
                body: body
            })

            if (response) {
                cart.value = response;
            }
        } catch (error: Error | any) {
            console.error("Erreur addCart:", error);
        } finally {
            isLoading.value = false;
        }
    }

    async function updateItemQuantity(itemId: number | string, newQuantity: number) {
        isLoading.value = true;
        try {
            const response = await $api('/cart/cart/update_item_quantity/', {
                method: 'POST',
                credentials: 'include', // Toujours pour les cookies
                body: {
                    item_id: itemId,
                    quantity: newQuantity
                }
            });
            // Le backend renvoie le panier mis à jour !
            cart.value = response;
        } catch (error) {
            console.error("Erreur lors de la mise à jour de la quantité:", error);
        } finally {
            isLoading.value = false;
        }
    }

    // 🔴 Action pour supprimer un article
    async function removeItem(itemId: number | string) {
        isLoading.value = true;
        try {
            const response = await $api('/cart/cart/remove_item/', {
                method: 'POST',
                credentials: 'include',
                body: {
                    item_id: itemId
                }
            });
            cart.value = response;
        } catch (error) {
            console.error("Erreur lors de la suppression de l'article:", error);
        } finally {
            isLoading.value = false;
        }
    }

    return{
        // Sate
        isLoading,
        cart,
        // Getters
        totalItems,
        fetchCart,
        addToCart,
        updateItemQuantity,
        removeItem
    }

})
