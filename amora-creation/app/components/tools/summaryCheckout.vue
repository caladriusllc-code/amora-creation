<template>
    <div class="checkout-summary">
        <h3>Résumé de la commande</h3>

        <div v-if="isGlobalLoading && cartItems.length === 0" class="loading-state">
            <p>Chargement de votre panier...</p>
        </div>

        <div v-else-if="cartItems.length === 0" class="empty-state">
            <p>Votre panier est vide.</p>
        </div>

        <div v-else class="summary-items-list">
            <div v-for="item in cartItems" :key="item.id || item.product.id" class="summary-item">
                <div class="item-image-wrapper">
                    <img :src="getCoverImage(item.product)" :alt="item.product.name" class="item-image" loading="lazy">
                    <span class="item-quantity-badge">{{ item.quantity }}</span>
                </div>
                
                <div class="item-details">
                    <h5 class="item-name">{{ item.product.name }}</h5>
                    <p class="item-variants">{{ item.size?.name || 'Taille unique' }}</p>
                    <span v-if="item.color" class="item-color-info">
                        <span v-if="item.color.hex_code" class="color-swatch" :style="{ backgroundColor: item.color.hex_code }" aria-hidden="true"></span>
                        Couleur : {{ item.color.name }}
                    </span>
                </div>

                <!-- ⚡️ NOUVEAU : Affichage du prix unitaire et du sous-total de la ligne -->
                <div class="item-price-container">
                    <p class="unit-price-calc">
                        {{ formatPrice(Number(item.product.price) || 0) }} 
                        <span class="qty-multiplier" v-if="item.quantity > 1">x {{ item.quantity }}</span>
                    </p>
                    <p class="item-subtotal">{{ formatPrice((Number(item.product.price) || 0) * item.quantity) }}</p>
                </div>
            </div>
        </div>

        <div class="summary-footer" v-if="cartItems.length > 0">
            <!-- ⚡️ NOUVEAU : Sous-total des articles seuls -->
            <div class="total-section sub-line">
                <span class="total-label sub-label">Sous-total</span>
                <span class="total-amount sub-amount">{{ formatPrice(cartSubtotal) }}</span>
            </div>

            <!-- Frais de livraison -->
            <div class="total-section sub-line" v-if="shippingFee > 0">
                <span class="total-label sub-label">Frais de livraison</span>
                <span class="total-amount sub-amount">{{ formatPrice(shippingFee) }}</span>
            </div>

            <hr class="summary-divider" />

            <!-- Total général recalculé -->
            <div class="total-section main-total">
                <span class="total-label">Total à payer</span>
                <span class="total-amount">{{ formatPrice(cartTotal) }}</span>
            </div>

            <!-- Dans summaryCheckout.vue, à l'intérieur de <div class="summary-footer"> -->

            <!-- ⚡️ NOUVEAU : Affichage du poids total du panier -->
            <div class="total-section sub-line" v-if="Number(cartStore.cart?.total_weight) > 0">
                <span class="total-label sub-label">Poids total estimé</span>
                <span class="total-amount sub-amount">{{ Number(cartStore.cart?.total_weight).toFixed(2) }} kg</span>
            </div>

            <!-- Frais de livraison (déjà existant) -->
            <div class="total-section sub-line" v-if="shippingFee > 0">
                <span class="total-label sub-label">Frais de livraison</span>
                <span class="total-amount sub-amount">{{ formatPrice(shippingFee) }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useCartStore } from '../../stores/cartStore'
import { useRuntimeConfig } from '#app'

const props = defineProps({
    shippingFee: {
        type: Number,
        default: 0
    }
});

const cartStore = useCartStore()
const config = useRuntimeConfig()

const cartItems = computed(() => cartStore.cart?.items || [])
const isGlobalLoading = computed(() => cartStore.isLoading)

// ⚡️ NOUVEAU : On sépare le sous-total (articles) du total final (articles + livraison)
const cartSubtotal = computed(() => {
    if (cartStore.cart?.total) {
        return Number(cartStore.cart.total);
    }
    return cartItems.value.reduce((total, item) => total + ((Number(item.product.price) || 0) * item.quantity), 0);
})

// ⚡️ NOUVEAU : Le total général est simplement le sous-total + la livraison
const cartTotal = computed(() => {
    return cartSubtotal.value + props.shippingFee;
})

const formatPrice = (price: number) => {
    return new Intl.NumberFormat('fr-FR').format(price) + ' FCFA'
}

const getCoverImage = (product: any) => {
    let imagePath = product.image || (product.images && product.images[0]?.image) || ''
    if (!imagePath) return 'https://via.placeholder.com/80'
    if (!imagePath.startsWith('http')) {
        const prefix = imagePath.startsWith('/') ? '' : '/'
        const apiBase = config.public.apiBase || 'http://localhost:8000'
        return `${apiBase}${prefix}${imagePath}`
    }
    return imagePath
}

onMounted(() => {
    if (cartItems.value.length === 0) {
        cartStore.fetchCart()
    }
})
</script>

<style scoped>
.checkout-summary { background-color: #fafafa; border: 1px solid #eaeaea; border-radius: 8px; padding: 24px; width: 100%; position: sticky; top: 24px; }
h3 { margin-top: 0; margin-bottom: 24px; font-size: 1.25rem; font-weight: 600; color: #111827; }
.loading-state, .empty-state { text-align: center; color: #6b7280; padding: 2rem 0; }
.summary-items-list { display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; }
.summary-item { display: flex; gap: 16px; align-items: center; }

.item-image-wrapper { position: relative; width: 64px; height: 80px; flex-shrink: 0; background: #eee; border-radius: 6px; border: 1px solid #eaeaea; }
.item-image { width: 100%; height: 100%; object-fit: cover; border-radius: 6px; }
.item-quantity-badge { position: absolute; top: -8px; right: -8px; background-color: #111827; color: #fff; font-size: 0.75rem; font-weight: bold; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }

.item-details { flex: 1; display: flex; flex-direction: column; gap: 4px; }
.item-name { margin: 0; font-size: 0.95rem; font-weight: 600; color: #1f2937; }
.item-variants { margin: 0; font-size: 0.8rem; color: #6b7280; }
.item-color-info { display: inline-flex; align-items: center; gap: 0.3rem; font-size: 0.8rem; color: #6b7280; }
.color-swatch { display: inline-block; width: 10px; height: 10px; border-radius: 50%; border: 1px solid rgba(0, 0, 0, 0.15); flex-shrink: 0; }

/* ⚡️ NOUVEAU : CSS pour aligner les prix et les sous-totaux par article */
.item-price-container { text-align: right; display: flex; flex-direction: column; justify-content: center; }
.unit-price-calc { font-size: 0.8rem; color: #6b7280; margin: 0 0 4px 0; }
.qty-multiplier { font-size: 0.75rem; color: #9ca3af; }
.item-subtotal { font-weight: 600; font-size: 1rem; color: #111827; margin: 0; }

/* ⚡️ NOUVEAU : CSS pour le footer et le séparateur */
.summary-footer { border-top: 1px solid #eaeaea; padding-top: 20px; }
.total-section { display: flex; justify-content: space-between; align-items: center; }
.sub-line { margin-bottom: 12px; }
.sub-label { font-size: 0.95rem; color: #4b5563; font-weight: 500; }
.sub-amount { font-size: 1rem; font-weight: 600; color: #374151; }

.summary-divider { border: none; border-top: 1px dashed #d1d5db; margin: 16px 0; }

.main-total { margin-top: 8px; }
.total-label { font-size: 1.15rem; color: #111827; font-weight: 700; }
.total-amount { font-size: 1.35rem; font-weight: 800; color: #000; }
</style>