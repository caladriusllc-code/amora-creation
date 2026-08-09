<template>
    <transition name="fade">
        <div class="cart-modale-overlay" v-if="isOpen" @click.self="$emit('close')">
            <div class="modale-content">
                
                <div class="modale-header">
                    <h4>Votre panier ({{ cartItems.length }})</h4>
                    <button class="close-button" @click="$emit('close')" aria-label="Fermer">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <div class="modale-body">
                    <div v-if="isGlobalLoading && cartItems.length === 0" class="empty-cart">
                        <p>Chargement...</p>
                    </div>

                    <div v-else-if="cartItems.length === 0" class="empty-cart w-full flex flex-col items-center justify-center gap-4">
                        <p>Votre panier est vide.</p>
                        <shopButton @click="$emit('close')" label="Continuer mes achats"/>
                    </div>
                    
                    <div class="cart-items-list" v-else>
                        <div v-for="item in cartItems" :key="item.id || item.product.id" 
                             class="cart-item"
                             :class="{ 'is-loading': loadingItemId === item.id }">
                            
                            <div class="item-image-wrapper">
                                <img :src="getCoverImage(item.product)" :alt="item.product.name" class="item-image" loading="lazy">
                            </div>
                            
                            <div class="item-details">
                                <h5 class="item-name">{{ item.product.name }}</h5>
                                <p class="item-variants">{{ item.product.size || 'Taille unique' }}</p>
                                
                                <div class="quantity-controls">
                                    <button @click="decreaseQuantity(item)" class="qty-btn" :disabled="loadingItemId === item.id">−</button>
                                    <span class="qty-number">{{ item.quantity }}</span>
                                    <button @click="increaseQuantity(item)" class="qty-btn" :disabled="loadingItemId === item.id">+</button>
                                </div>
                            </div>

                            <div class="item-actions">
                                <p class="item-price">{{ formatPrice(item.product.price * item.quantity) }}</p>
                                <button class="remove-btn" @click="removeItem(item)" :disabled="loadingItemId === item.id">
                                    Supprimer
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="modale-footer" v-if="cartItems.length > 0 && !isGlobalLoading">
                    <div class="total-section">
                        <span class="total-label">Total :</span>
                        <span class="total-amount">{{ formatPrice(cartTotal) }}</span>
                    </div>
                    <button 
                        class="checkout-button" 
                        @click="()=> {router.push('/order')}" 
                        >
                            Commander
                        </button>
                </div>
            </div>
        </div>
    </transition>
</template>

<script lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useCartStore } from '../../stores/cartStore';
import { useRouter } from 'vue-router'
import shopButton from '../buttons/shopButton.vue'

export default {

    components:{ shopButton},
    props: {
        isOpen: { type: Boolean, default: false }
    },
    emits: ['close'],
    
    setup() {

        const router = useRouter();

        const cartStore = useCartStore();
        
        // État de chargement léger par article
        const loadingItemId = ref<number | string | null>(null);

        const cartItems = computed(() => cartStore.cart?.items || []);
        
        const cartTotal = computed(() => {
            if (cartStore.cart?.total) return cartStore.cart.total;
            return cartItems.value.reduce((total, item) => total + ((item.product.price || 0) * item.quantity), 0);
        });

        const isGlobalLoading = computed(() => cartStore.isLoading);

        const formatPrice = (price: number) => {
            return new Intl.NumberFormat('fr-FR').format(price) + ' FCFA';
        };

        const getCoverImage = (product: any) => {
            let imagePath = product.image || (product.images && product.images[0]?.image) || '';
            if (!imagePath) return 'https://via.placeholder.com/80';
            if (!imagePath.startsWith('http')) {
                const prefix = imagePath.startsWith('/') ? '' : '/';
                return `http://localhost:8000${prefix}${imagePath}`;
            }
            return imagePath;
        };

        const increaseQuantity = async (item: any) => {
            loadingItemId.value = item.id;
            await cartStore.updateItemQuantity(item.id, item.quantity + 1);
            loadingItemId.value = null;
        };

        const decreaseQuantity = async (item: any) => {
            loadingItemId.value = item.id;
            if (item.quantity - 1 > 0) {
                await cartStore.updateItemQuantity(item.id, item.quantity - 1);
                loadingItemId.value = null;
            } else {
                await removeItem(item);
            }
        };

        const removeItem = async (item: any) => {
            loadingItemId.value = item.id;
            await cartStore.removeItem(item.id);
            loadingItemId.value = null;
        };

        onMounted(() => {
            cartStore.fetchCart();
        });

        return { 
            router,
            cartItems, cartTotal, isGlobalLoading, loadingItemId,
            formatPrice, getCoverImage, increaseQuantity, decreaseQuantity, removeItem
        };
    }
}
</script>

<style scoped>
/* ======= OVERLAY SANS FLOU (Performant) ======= */
.cart-modale-overlay {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.65); /* Fond simplement assombri */
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* ======= BOITE CENTRALE ======= */
.modale-content {
    background-color: #fff;
    border-radius: 8px;
    width: 90%;
    height: 80vh; 
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15); /* Ombre légère */
}

@media (min-width: 992px) {
    .modale-content { width: 450px; max-height: 85vh; }
}

/* ======= HEADER ======= */
.modale-header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 1.2rem; border-bottom: 1px solid #eee;
}
.modale-header h4 { margin: 0; font-size: 1.1rem; font-weight: 600; }
.close-button {
    background: none; border: none; cursor: pointer; color: #333;
    padding: 0.5rem; display: flex; align-items: center; justify-content: center;
}
.close-button svg { width: 20px; height: 20px; }

/* ======= BODY ======= */
.modale-body {
    flex: 1; overflow-y: auto; padding: 1.2rem;
}

.empty-cart { text-align: center; color: #666; margin-top: 2rem; }
.continue-btn {
    margin-top: 1rem; padding: 0.6rem 1.2rem;
    background: #f5f5f5; border: 1px solid #ddd; border-radius: 4px;
    cursor: pointer; color: #333;
}

/* ======= ARTICLES ======= */
.cart-items-list { display: flex; flex-direction: column; gap: 1rem; }
.cart-item {
    display: flex; gap: 1rem; align-items: center;
    padding-bottom: 1rem; border-bottom: 1px solid #f9f9f9;
}
.cart-item:last-child { border-bottom: none; }

/* ÉTAT CHARGEMENT ULTRA LÉGER */
.is-loading { opacity: 0.4; pointer-events: none; }

.item-image-wrapper { width: 70px; height: 90px; flex-shrink: 0; background: #eee; }
.item-image { width: 100%; height: 100%; object-fit: cover; }

.item-details { flex: 1; display: flex; flex-direction: column; gap: 0.2rem; }
.item-name { margin: 0; font-size: 0.95rem; font-weight: 600; }
.item-variants { margin: 0; font-size: 0.8rem; color: #666; }

.quantity-controls {
    display: flex; align-items: center; gap: 0.8rem;
    margin-top: 0.3rem; border: 1px solid #ddd; width: fit-content; padding: 0.1rem 0.4rem;
}
.qty-btn { background: none; border: none; cursor: pointer; font-size: 1.1rem; color: #333; }
.qty-number { font-size: 0.9rem; min-width: 15px; text-align: center; }

.item-actions { display: flex; flex-direction: column; align-items: flex-end; gap: 0.5rem; }
.item-price { margin: 0; font-weight: 600; font-size: 1rem; }
.remove-btn { background: none; border: none; cursor: pointer; font-size: 0.8rem; color: #999; text-decoration: underline; padding: 0; }

/* ======= FOOTER ======= */
.modale-footer {
    padding: 1.2rem; border-top: 1px solid #eee; background: #fafafa;
}
.total-section { display: flex; justify-content: space-between; margin-bottom: 1rem; }
.total-label { font-size: 1rem; color: #666; }
.total-amount { font-size: 1.2rem; font-weight: 700; }

.checkout-button {
    width: 100%; background: #000; color: #fff; border: none;
    padding: 1rem; border-radius: 4px; font-weight: 600; cursor: pointer;
}

/* ANIMATION BASIQUE D'OUVERTURE */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>