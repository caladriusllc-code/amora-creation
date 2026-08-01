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
                <div v-if="isLoading" class="empty-cart">
                    <p>Chargement de votre panier...</p>
                </div>

                <div v-else-if="cartItems.length === 0" class="empty-cart">
                    <p>Votre panier est actuellement vide.</p>
                </div>
                
                <div v-else class="cart-items-list">
                    <div v-for="item in cartItems" :key="item.product.id" class="cart-item">
                        <div class="item-image-wrapper">
                            <img :src="getCoverImage(item.product)" :alt="item.product.name" class="item-image">
                        </div>
                        
                        <div class="item-details">
                            <h5 class="item-name">{{ item.product.name }}</h5>
                            <p class="item-variants">Taille: {{ item.product.size || 'N/A' }} | Couleur: {{ item.product.color || 'N/A' }}</p>
                            
                            <div class="quantity-controls">
                                <button @click="decreaseQuantity(item)" class="qty-btn" :disabled="isLoading">-</button>
                                <span class="qty-number">{{ item.quantity }}</span>
                                <button @click="increaseQuantity(item)" class="qty-btn" :disabled="isLoading">+</button>
                            </div>
                        </div>

                        <div class="item-actions">
                            <p class="item-price">{{ formatPrice(item.product.price * item.quantity) }}</p>
                            <button class="remove-btn" @click="removeItem(item)" :disabled="isLoading">Supprimer</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="modale-footer" v-if="cartItems.length > 0 && !isLoading">
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
import { computed, onMounted } from 'vue';
import { useCartStore } from '../../stores/cartStore'; // <-- ASSURE-TOI QUE CE CHEMIN EST CORRECT

export default {
    props: {
        isOpen: {
            type: Boolean,
            default: false
        }
    },
    // On garde les emits : ce sera le composant parent qui appellera les futures actions du store (ajouter, supprimer...)
    emits: ['close', 'increase', 'decrease', 'remove'],
    
    setup(props) {
        // 1. Initialisation du store
        const cartStore = useCartStore();

        // 2. Récupération réactive des données du store
        const cartItems = computed(() => cartStore.cart?.items || []);
        
        // On utilise la propriété "total" de ton interface Cart. Si elle n'existe pas, on fait le calcul de secours.
        const cartTotal = computed(() => {
            if (cartStore.cart?.total) {
                return cartStore.cart.total;
            }
            // Secours si le backend n'a pas encore renvoyé le total
            return cartItems.value.reduce((total, item) => total + ((item.product.price || 0) * item.quantity), 0);
        });

        const isLoading = computed(() => cartStore.isLoading);

        // 3. Formateur de prix
        const formatPrice = (price: number) => {
            return new Intl.NumberFormat('fr-FR').format(price) + ' FCFA';
        };

        // 4. Fonction pour récupérer la bonne image du produit ✨
        const getCoverImage = (product: any) => {
            let imagePath = '';
            
            // 1. On extrait le chemin de l'image
            if (product.image && typeof product.image === 'string') {
                imagePath = product.image;
            } else if (product.images && product.images.length > 0) {
                imagePath = product.images[0].image || product.images[0].url || product.images[0];
            }

            // 2. Si on n'a rien trouvé, on met un placeholder
            if (!imagePath) {
                return 'https://via.placeholder.com/150?text=Pas+d%27image';
            }

            // 3. LA CORRECTION : Si l'URL ne commence pas par http (donc c'est un chemin relatif)
            if (!imagePath.startsWith('http')) {
                // Si l'URL ne commence pas par un slash, on l'ajoute
                const prefix = imagePath.startsWith('/') ? '' : '/';
                
                // On ajoute l'adresse de ton backend Django (ajuste si tu as configuré un dossier /media/ spécifique)
                // Note : si ton image est dans le dossier media, l'URL finale devrait ressembler à http://localhost:8000/media/products/...
                
                // Si Django ne renvoie pas /media/ dans le JSON, décommente la ligne du bas et commente l'autre :
                // return `http://localhost:8000/media${prefix}${imagePath}`;
                
                return `http://localhost:8000${prefix}${imagePath}`;
            }

            return imagePath;
        };

        // 5. On va mettre à jour les quantités diminuer ou augmenter
        const increaseQuantity = async (item: any) => {
            // On calcule la nouvelle quantité et on utilise l'ID de l'item (CartItem ID)
            const newQuantity = item.quantity + 1;
            await cartStore.updateItemQuantity(item.id, newQuantity);
        };

        const decreaseQuantity = async (item: any) => {
            const newQuantity = item.quantity - 1;
            // Si la quantité tombe à 0, on supprime l'article
            if (newQuantity > 0) {
                await cartStore.updateItemQuantity(item.id, newQuantity);
            } else {
                await cartStore.removeItem(item.id);
            }
        };

        const removeItem = async (item: any) => {
            await cartStore.removeItem(item.id);
        };

        onMounted(()=> {
            // On va déclencher le panier au montage du composant
            cartStore.fetchCart();
            console.log("Cart monté et fetché", cartStore.cart)
        })

        return { 
            cartItems, 
            cartTotal, 
            isLoading, 
            formatPrice,
            getCoverImage,
            increaseQuantity,
            decreaseQuantity,
            removeItem
        };
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