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

            <div v-show="showScrollbar && secondaryImages.length > 0" class="custom-scrollbar-container">
                <div class="scrollbar-track" ref="trackRef" @click="handleTrackClick">
                    <div
                    class="scrollbar-thumb"
                    :style="{ width: `${thumbWidth}%`, left: `${thumbLeft}%` }"
                    @mousedown.prevent="startDrag"
                    @touchstart="startDrag"
                    ></div>
                </div>
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
import type { Product } from '../../stores/productStore'

import productGrid from '../layout/productGrid.vue';
import productCategory from '../layout/productsCategory.vue'
import cartButton from '../buttons/cartButton.vue'
import productSizes from '../tools/productSizes.vue'
import productColors from '../tools/productColors.vue'
import shopButton from '../buttons/shopButton.vue'

export default {
    components: {
        productGrid,
        productCategory,
        cartButton,
        productSizes,
        productColors,
        shopButton
    },
    emits: ['addToCart'],
    setup() {
        const route = useRoute();
        const productStore = useProductStore();
        const cartStore = useCartStore();

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

        // --- Refs pour le scrolling (inchangé) ---
        const cardsContainer = ref<HTMLElement | null>(null);
        const trackRef = ref<HTMLElement | null>(null);
        const thumbWidth = ref(0);
        const thumbLeft = ref(0);
        const showScrollbar = ref(false);
        let isDragging = false;
        let startX = 0;
        let startScrollLeft = 0;

        const updateScrollbar = () => {
            const container = cardsContainer.value;
            if (!container) return;
            const { scrollLeft, scrollWidth, clientWidth } = container;
            if (scrollWidth <= clientWidth) {
                showScrollbar.value = false;
                return;
            }
            showScrollbar.value = true;
            const visibleRatio = clientWidth / scrollWidth;
            const calculatedWidth = Math.max(10, Math.min(100, visibleRatio * 100));
            thumbWidth.value = calculatedWidth;
            const maxScrollLeft = scrollWidth - clientWidth;
            const progress = maxScrollLeft > 0 ? scrollLeft / maxScrollLeft : 0;
            thumbLeft.value = progress * (100 - calculatedWidth);
        };

        const startDrag = (e: MouseEvent | TouchEvent) => {
            e.preventDefault();
            const container = cardsContainer.value;
            if (!container) return;
            isDragging = true;
            const clientX = e instanceof MouseEvent ? e.clientX : e.touches[0].clientX;
            startX = clientX;
            startScrollLeft = container.scrollLeft;
            document.addEventListener('mousemove', onDrag);
            document.addEventListener('mouseup', stopDrag);
            document.addEventListener('touchmove', onDrag, { passive: false });
            document.addEventListener('touchend', stopDrag);
        };

        const onDrag = (e: MouseEvent | TouchEvent) => {
            if (!isDragging) return;
            e.preventDefault();
            const container = cardsContainer.value;
            const track = trackRef.value;
            if (!container || !track) return;
            const clientX = e instanceof MouseEvent ? e.clientX : e.touches[0].clientX;
            const deltaX = clientX - startX;
            const trackWidth = track.offsetWidth;
            const maxScrollLeft = container.scrollWidth - container.clientWidth;
            const ratio = maxScrollLeft / (trackWidth * (1 - thumbWidth.value / 100));
            container.scrollLeft = startScrollLeft + deltaX * ratio;
        };

        const stopDrag = () => {
            if (!isDragging) return;
            isDragging = false;
            document.removeEventListener('mousemove', onDrag);
            document.removeEventListener('mouseup', stopDrag);
            document.removeEventListener('touchmove', onDrag);
            document.removeEventListener('touchend', stopDrag);
        };

        const handleTrackClick = (e: MouseEvent) => {
            const container = cardsContainer.value;
            const track = trackRef.value;
            if (!container || !track) return;
            const rect = track.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const trackWidth = rect.width;
            const thumbWidthPx = (thumbWidth.value / 100) * trackWidth;
            const maxScrollLeft = container.scrollWidth - container.clientWidth;
            const targetScroll = ((clickX - thumbWidthPx / 2) / (trackWidth - thumbWidthPx)) * maxScrollLeft;
            container.scrollTo({
                left: Math.max(0, Math.min(targetScroll, maxScrollLeft)),
                behavior: 'smooth',
            });
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
            try{
                if (product.value?.id){
                    // Passer la taille et couleur sélectionnées
                    await cartStore.addToCart(
                        product.value.id,
                        1,
                        selectedSize.value?.id,
                        selectedColor.value?.id
                    )
                }

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

            const container = cardsContainer.value;
            if (container) {
                container.addEventListener('scroll', updateScrollbar);
                setTimeout(() => updateScrollbar(), 100);
            }
        });

        return {
            product,
            currentMainImage,
            secondaryImages,
            setMainImage,
            selectedSize,
            selectedColor,
            onSizeSelected,
            onColorSelected,

            cardsContainer,
            trackRef,
            thumbWidth,
            thumbLeft,
            showScrollbar,
            startDrag,
            handleTrackClick,
            updateScrollbar,
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
