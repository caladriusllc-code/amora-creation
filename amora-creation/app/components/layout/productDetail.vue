<template>
    <div v-if="product" class="product-detail-layout">

        <div class="pic-detail-layout">
            <article class="main-pic">
                <img :src="currentMainImage" :alt="product.name">
            </article>

            <div ref="cardsContainer" class="cards-layout" v-if="secondaryImages.length > 0">
                <article
                    v-for="img in secondaryImages"
                    :key="img.id"
                    class="second-pic"
                    @click="setMainImage(img.image)"
                    style="cursor: pointer;"
                >
                    <img :src="img.image" :alt="product.name">
                </article>
            </div>
        </div>

        <div class="info-detail-layout">
            <div class="product-detail">
                <h2 class="product-name">{{ product.name }}</h2>
                <p class="product-description">{{ product.description }}</p>

                <div class="buy-section">
                    <p class="product-price">
                        {{ product.discount_price ? product.discount_price : product.price }} FCFA
                    </p>
                </div>
                <shopButton @click="addToCart()"/>
            </div>

            <productSizes :sizes="product.sizes" @size-selected="onSizeSelected" />
            <productColors :colors="product.colors" @color-selected="onColorSelected" />

            <inStockTool 
                :is-in-stock="product.is_in_stock"
            />

            <instockModal 
                :is-open="showStockModal"
                :product-name="name"
                @close="showStockModal = false"
            />

        </div>

    </div>

    <div v-else class="loading-state">
        <p>Chargement des détails du produit...</p>
    </div>
</template>

<script lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useProductStore } from '../../stores/productStore';
import { useCartStore } from '../../stores/cartStore'

import productGrid from '../layout/productGrid.vue';
import productCategory from '../layout/productsCategory.vue'
import cartButton from '../buttons/cartButton.vue'
import productSizes from '../tools/productSizes.vue'
import productColors from '../tools/productColors.vue'
import shopButton from '../buttons/shopButton.vue'
import instockModal from '../modale/instockModal.vue';
import inStockTool from '../tools/inStockTool.vue';

export default {
    components: {
        productGrid,
        productCategory,
        cartButton,
        productSizes,
        productColors,
        shopButton,
        instockModal,
        inStockTool
    },
    props:{
        name:String,
        basePrice: [Number, String],
        isInStock:{
            type:Boolean,
            default: true
        }
    },
    emits: ['addToCart'],
    setup(_props, { emit }) {
        const route = useRoute();
        const productStore = useProductStore();
        const cartStore = useCartStore();

        // About inStockModale
        const showStockModal = ref(false);
        

        const product = computed(() => {
            const slug = route.params.slug;
            return productStore.products.find(p => p.slug === slug);
        });

        // 🛠️ NOUVEAU : Une variable pour stocker l'image sélectionnée au clic
        const selectedImage = ref<string | null>(null);

        // 🛠️ MODIFIÉ : L'image principale affiche "selectedImage" si elle existe, sinon elle prend l'image par défaut
        const currentMainImage = computed(() => {
            if (selectedImage.value) return selectedImage.value;

            if (!product.value?.images?.length) return 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80';
            const main = product.value.images.find(img => img.is_main);
            return main ? main.image : product.value.images[0].image;
        });

        // 🛠️ MODIFIÉ : Les miniatures affichent toutes les images SAUF celle qui est actuellement en grand
        const secondaryImages = computed(() => {
            if (!product.value?.images?.length) return [];
            return product.value.images.filter(img => img.image !== currentMainImage.value);
        });

        // 🛠️ NOUVEAU : Fonction appelée lors du clic sur une miniature
        const setMainImage = (imageUrl: string) => {
            selectedImage.value = imageUrl;
        };

        // Logique pour ajouter le produit au panier
        const selectedSize = ref<any>(null);
        const selectedColor = ref<any>(null);

        const onSizeSelected = (size: any) => {
            selectedSize.value = size;
            console.log('Taille sélectionnée:', size);
        };

        const onColorSelected = (color: any) => {
            selectedColor.value = color;
            console.log('Couleur sélectionnée:', color);
        };

        async function addToCart(){
            if (!product.value) return;

            if (!product.value.is_in_stock){
                showStockModal.value = true;
                return;
            }

            try{
                // Passer la taille et couleur sélectionnées
                await cartStore.addToCart(
                    product.value.id,
                    1,
                    selectedSize.value?.id,
                    selectedColor.value?.id
                )

                emit('addToCart');
                return cartStore.cart;
            } catch(error: any){
                console.error('Erreur lors de l\'ajout au panier:', error);
                throw new Error(error.message || 'Erreur inconnue lors de l\'ajout au panier');
            }
        }

        onMounted(async () => {
            if (!productStore.products.length) {
                await productStore.fetchProducts();
            }
        });

        return {
            product,
            showStockModal,
            currentMainImage,
            secondaryImages,
            setMainImage,
            selectedSize,
            selectedColor,
            onSizeSelected,
            onColorSelected,
            addToCart,
            cartStore
        };
    }
}
</script>

<style scoped>
/* =========================================
   STYLES MOBILE (Téléphone) - Par défaut
   ========================================= */

.product-detail-layout {
    padding-top:2rem;
    display: flex;
    flex-direction: column;
    width: 100%;
    min-height: 100vh;
}

.pic-detail-layout {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 100%;
    padding: 0.2rem;
}

.main-pic {
    width: 100%;
    display: block; /* S'assure que le conteneur existe bien */
}

.main-pic img {
    width: 100%;
    max-width: 100%; /* Empêche l'image de déborder */
    height: auto;
    object-fit: cover;
    border-radius: 8px;
    display: block; /* Enlève les marges invisibles sous l'image */
}

/* Nouveau conteneur pour la colonne de droite */
.info-detail-layout {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 1.5rem; /* Espace entre les textes, les tailles et les couleurs */
}

.product-detail {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.product-name {
    font-size: 1.5rem;
    font-weight: 500;
}

.cards-layout {
    display: flex;
    flex-direction: row;
    overflow-x: auto;
    width: 100%;
    gap: 12px;
    padding: 5px;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.cards-layout::-webkit-scrollbar {
    display: none;
}

.second-pic {
    flex-shrink: 0;
    width: 45%;
    height: 220px;
}

.second-pic img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px;
}

.custom-scrollbar-container {
    width: 100%;
    height: 6px;
    background-color: #f0f0f0;
    margin-top: 10px;
    border-radius: 4px;
    position: relative;
}

.scrollbar-track {
    width: 100%;
    height: 100%;
    position: relative;
    cursor: pointer;
}

.scrollbar-thumb {
    height: 100%;
    background-color: #333;
    border-radius: 4px;
    position: absolute;
    top: 0;
}

.product-price {
    font-weight: 900;
    color: #111827;
    font-size: 18px;
    margin: 0;
}

.buy-section {
    width: 100%;
    display: flex;
    justify-content: start;
    align-items: center;
    gap: 1rem;
}

/* =========================================
   STYLES DESKTOP / LAPTOP (Écrans larges)
   ========================================= */
@media (min-width: 768px) {
    .product-detail-layout {
        flex-direction: row; /* Aligne la colonne image et la colonne info côte à côte */
        align-items: center;
        justify-content: space-around;
        max-width: 1200px;
        margin: 0 auto;
        padding-top: 8rem;
        gap: 2rem; /* Espacement aéré entre l'image et les infos */
    }

    .pic-detail-layout {
        flex-direction: row;
        align-items: flex-start;
        width: 50%; /* La colonne image prend 50% */
        gap: 1rem; /* Espace entre l'image principale et les miniatures */
        padding: 0;
    }

    .main-pic {
        flex: 1;
        width: 100%;
        min-width: 300px; /* Force Flexbox à ne JAMAIS écraser l'image en dessous de 300px */
        margin-bottom: 0;
    }

    /* Le nouveau conteneur prend l'autre moitié de l'écran */
    .info-detail-layout {
        width: 50%;
        padding-top: 0; /* Aligne avec le haut de l'image */
    }

    .cards-layout {
        flex-direction: column;
        overflow-y: auto;
        overflow-x: hidden;
        height: 100%;
        max-height: 600px; /* Limite la hauteur de la colonne de miniatures */
        padding: 0;
        gap: 1rem;
    }

    .second-pic {
        width: 100px;
        height: 140px; /* Ajuste la hauteur des miniatures sur ordinateur */
        margin-bottom: 0;
    }

    .custom-scrollbar-container {
        display: none;
    }

    /* Réinitialise les padding inutiles puisque le parent info-detail-layout gère l'espacement */
    .product-detail {
        width: 100%;
        padding: 0;
    }
}
</style>
