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
                    <!-- ⚡️ Sécurisation avec le chaînage optionnel (?.) -->
                    <p class="item-variants">{{ item.size?.name || 'Taille unique' }}</p>
                    <span v-if="item.color" class="item-color-info">
                        <span
                            v-if="item.color.hex_code"
                            class="color-swatch"
                            :style="{ backgroundColor: item.color.hex_code }"
                            aria-hidden="true"
                        ></span>
                        Couleur : {{ item.color.name }}
                    </span>
                </div>

                <div class="item-price">
                    <!-- ⚡️ Conversion numérique forcée pour éviter les erreurs NaN -->
                    <p>{{ formatPrice((Number(item.product.price) || 0) * item.quantity) }}</p>
                </div>
                
            </div>
        </div>

        <div class="summary-footer" v-if="cartItems.length > 0">
            <div class="total-section">
                <span class="total-label">Total à payer</span>
                <span class="total-amount">{{ formatPrice(cartTotal) }}</span>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useCartStore } from '../../stores/cartStore'
import { useRuntimeConfig } from '#app'

const cartStore = useCartStore()
const config = useRuntimeConfig()

// --- COMPUTED PROPERTIES ---
const cartItems = computed(() => cartStore.cart?.items || [])
const isGlobalLoading = computed(() => cartStore.isLoading)

const cartTotal = computed(() => {
    if (cartStore.cart?.total) return cartStore.cart.total
    // ⚡️ Conversion numérique appliquée ici aussi
    return cartItems.value.reduce((total, item) => total + ((Number(item.product.price) || 0) * item.quantity), 0)
})

// --- MÉTHODES ---
const formatPrice = (price: number) => {
    return new Intl.NumberFormat('fr-FR').format(price) + ' FCFA'
}

const getCoverImage = (product: any) => {
    let imagePath = product.image || (product.images && product.images[0]?.image) || ''
    if (!imagePath) return 'https://via.placeholder.com/80'
    if (!imagePath.startsWith('http')) {
        const prefix = imagePath.startsWith('/') ? '' : '/'
        // ⚡️ Utilisation des variables d'environnement (avec fallback localhost)
        const apiBase = config.public.apiBase || 'http://localhost:8000'
        return `${apiBase}${prefix}${imagePath}`
    }
    return imagePath
}

// S'assurer que le panier est chargé si l'utilisateur arrive directement sur cette page
onMounted(() => {
    if (cartItems.value.length === 0) {
        cartStore.fetchCart()
    }
})
</script>

<style scoped>
.checkout-summary {
    background-color: #fafafa;
    border: 1px solid #eaeaea;
    border-radius: 8px;
    padding: 24px;
    width: 100%;
    /* Idéal pour rester collé en haut lors du scroll sur grand écran */
    position: sticky;
    top: 24px; 
}

h3 {
    margin-top: 0;
    margin-bottom: 24px;
    font-size: 1.25rem;
    font-weight: 600;
    color: #333;
}

.loading-state, .empty-state {
    text-align: center;
    color: #666;
    padding: 2rem 0;
}

/* ======= ARTICLES ======= */
.summary-items-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 24px;
}

.summary-item {
    display: flex;
    gap: 16px;
    align-items: center;
}

.item-image-wrapper {
    position: relative;
    width: 64px;
    height: 80px;
    flex-shrink: 0;
    background: #eee;
    border-radius: 6px;
    border: 1px solid #eaeaea;
}

.item-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
}

.item-quantity-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background-color: #000; /* Couleur Amora */
    color: #fff;
    font-size: 0.75rem;
    font-weight: bold;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}

.item-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.item-name {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 600;
    color: #333;
}

.item-variants {
    margin: 0;
    font-size: 0.8rem;
    color: #666;
}

.item-price {
    font-weight: 600;
    font-size: 0.95rem;
    color: #333;
}

/* ======= FOOTER ======= */
.summary-footer {
    border-top: 1px solid #eaeaea;
    padding-top: 20px;
}

.total-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.total-label {
    font-size: 1.1rem;
    color: #333;
    font-weight: 600;
}

.total-amount {
    font-size: 1.25rem;
    font-weight: 700;
    color: #000;
}

.item-color-info { display: inline-flex; align-items: center; gap: 0.3rem; }
.color-swatch {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    border: 1px solid rgba(0, 0, 0, 0.15);
    flex-shrink: 0;
}

</style>