<template>
    <div class="cart-modale-overlay" v-if="isOpen">
        <div class="modale-content">
            <div class="modale-header">
                <h4>Votre panier ({{ cartItems.length }})</h4>
                <button class="close-button" @click="$emit('close')">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <div class="modale-body">
                <div v-if="cartItems.length === 0" class="empty-cart">
                    <p>Votre panier est actuellement vide.</p>
                </div>
                
                <div v-else class="cart-items-list">
                    <div v-for="item in cartItems" :key="item.id" class="cart-item">
                        <div class="item-image-wrapper">
                            <img :src="item.image" :alt="item.name" class="item-image">
                        </div>
                        
                        <div class="item-details">
                            <h5 class="item-name">{{ item.name }}</h5>
                            <p class="item-variants">Taille: {{ item.size }} | Couleur: {{ item.color }}</p>
                            
                            <div class="quantity-controls">
                                <button @click="$emit('decrease', item.id)" class="qty-btn">-</button>
                                <span class="qty-number">{{ item.quantity }}</span>
                                <button @click="$emit('increase', item.id)" class="qty-btn">+</button>
                            </div>
                        </div>

                        <div class="item-actions">
                            <p class="item-price">{{ formatPrice(item.price * item.quantity) }}</p>
                            <button class="remove-btn" @click="$emit('remove', item.id)">Supprimer</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modale-footer" v-if="cartItems.length > 0">
                <div class="total-section">
                    <span class="total-label">Total :</span>
                    <span class="total-amount">{{ formatPrice(cartTotal) }}</span>
                </div>
                <button class="checkout-button">Passer la commande</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { computed } from 'vue';

export default {
    props: {
        isOpen: {
            type: Boolean,
            default: false
        },
        // Nouvelle prop pour recevoir les articles du panier
        cartItems: {
            type: Array,
            // Données factices pour tester le visuel (à retirer une fois connecté à tes vraies données)
            default: () => [
                { id: 1, name: "Robe d'été Élégance", size: "M", color: "Noir", price: 12000, quantity: 1, image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=200&q=80" },
                { id: 2, name: "Veste en Jean Amora", size: "L", color: "Bleu", price: 25000, quantity: 2, image: "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=200&q=80" }
            ]
        }
    },
    emits: ['close', 'increase', 'decrease', 'remove'],
    setup(props) {
        // Calcule le total du panier automatiquement
        const cartTotal = computed(() => {
            return props.cartItems.reduce((total: any, item: any) => total + (item.price * item.quantity), 0);
        });

        // Formate le prix avec "FCFA" et des espaces (ex: 12 000 FCFA)
        const formatPrice = (price: number) => {
            return new Intl.NumberFormat('fr-FR').format(price) + ' FCFA';
        };

        return { cartTotal, formatPrice };
    }
}
</script>

<style scoped>
/* ======= FOND DE LA MODALE ======= */
.cart-modale-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* ======= BOITE CENTRALE ======= */
.modale-content {
    background-color: white;
    border-radius: 12px;
    width: 90%;
    height: 80vh; 
    display: flex;
    flex-direction: column; /* Organise le header, body et footer en colonne */
    overflow: hidden; /* Empêche la modale entière de scroller */
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

@media (min-width: 992px) {
    .modale-content {
        width: 500px; /* Plus fin et plus élégant sur ordinateur */
        max-height: 80vh;
    }
}

/* ======= HEADER ======= */
.modale-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #f0f0f0;
}
.modale-header h4 {
    margin: 0;
    font-size: 1.2rem;
    font-weight: 600;
    text-transform: uppercase;
}
.close-button {
    background: none;
    border: none;
    cursor: pointer;
    color: #666;
}
.close-button svg { width: 24px; height: 24px; }

/* ======= BODY (La zone de scroll) ======= */
.modale-body {
    flex: 1; /* Prend tout l'espace disponible entre le header et le footer */
    overflow-y: auto; /* Active le scroll uniquement ici ! */
    padding: 1.5rem;
}

.empty-cart {
    text-align: center;
    color: #6b7280;
    margin-top: 2rem;
}

/* ======= LES ARTICLES (Cart Items) ======= */
.cart-items-list {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.cart-item {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.item-image-wrapper {
    width: 80px;
    height: 100px;
    flex-shrink: 0;
}
.item-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 6px;
}

.item-details {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
}
.item-name {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: #111;
}
.item-variants {
    margin: 0;
    font-size: 0.85rem;
    color: #6b7280;
}

/* Boutons de Quantité (+ / -) */
.quantity-controls {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-top: 0.5rem;
    border: 1px solid #e5e7eb;
    width: fit-content;
    border-radius: 4px;
    padding: 0.2rem;
}
.qty-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 1.1rem;
    padding: 0 0.5rem;
    color: #111;
}
.qty-number { font-size: 0.9rem; font-weight: 500; }

/* Prix et bouton supprimer */
.item-actions {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.5rem;
}
.item-price {
    margin: 0;
    font-weight: 700;
    font-size: 1rem;
    color: #111;
}
.remove-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 0.8rem;
    color: #ef4444; /* Rouge doux */
    text-decoration: underline;
    padding: 0;
}

/* ======= FOOTER ======= */
.modale-footer {
    padding: 1.5rem;
    border-top: 1px solid #f0f0f0;
    background-color: #fafafa;
}

.total-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}
.total-label { font-size: 1.1rem; font-weight: 500; color: #374151; }
.total-amount { font-size: 1.3rem; font-weight: 900; color: #111; }

.checkout-button {
    width: 100%;
    background-color: #000;
    color: #fff;
    border: none;
    padding: 1rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
.checkout-button:hover {
    background-color: #333;
}
</style>