<template>
    <div class="product-detail-layout">
        <div class="pic-detail-layout">
            <article class="main-pic">
                <img 
                    src="../../assets/fashion/BCO.04e39cd1-7c12-4a5e-81ee-5dfdfb1782a1.png" alt=""
                >
            </article>
            
            <div ref="cardsContainer" class="cards-layout">
                <article class="second-pic">
                    <img src="../../assets/fashion/BCO.04e39cd1-7c12-4a5e-81ee-5dfdfb1782a1.png" alt="">
                </article>
                <article class="second-pic">
                    <img src="../../assets/fashion/BCO.04e39cd1-7c12-4a5e-81ee-5dfdfb1782a1.png" alt="">
                </article>
                <article class="second-pic">
                    <img src="../../assets/fashion/BCO.04e39cd1-7c12-4a5e-81ee-5dfdfb1782a1.png" alt="">
                </article>
                <article class="second-pic">
                    <img src="../../assets/fashion/BCO.04e39cd1-7c12-4a5e-81ee-5dfdfb1782a1.png" alt="">
                </article>
            </div>

            <div v-show="showScrollbar" class="custom-scrollbar-container">
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
        <div class="product-detail">
            <h1 class="product-name">Robe d'été Élégance</h1>
            <p class="product-price">12 000 FCFA</p>
            <p class="product-description">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                Quisquam, quod. Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                Quisquam, quod.
            </p>
            <button class="add-to-cart-btn">Ajouter au panier</button>
        </div>
    </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import productGrid from '../layout/productGrid.vue';
import productCategory from '../layout/productsCategory.vue'
export default {
    components:{
        productGrid,
        productCategory
    },
    setup() {
        // Refs pour le scrolling
        const cardsContainer = ref<HTMLElement | null>(null);
        const trackRef = ref<HTMLElement | null>(null);

        // Scrollbar state
        const thumbWidth = ref(0);
        const thumbLeft = ref(0);
        const showScrollbar = ref(false);

        // État pour le drag
        let isDragging = false;
        let startX = 0;
        let startScrollLeft = 0;

        // Met à jour la position et la taille du curseur
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

        // Démarre le drag du curseur
        const startDrag = (e: MouseEvent | TouchEvent) => {
            e.preventDefault();
            const container = cardsContainer.value;
            if (!container) return;

            isDragging = true;

            // Récupère la coordonnée X de l'événement (souris ou tactile)
            const clientX = e instanceof MouseEvent ? e.clientX : e.touches[0].clientX;
            startX = clientX;
            startScrollLeft = container.scrollLeft;

            // Ajoute les écouteurs globaux pour suivre le mouvement
            document.addEventListener('mousemove', onDrag);
            document.addEventListener('mouseup', stopDrag);
            document.addEventListener('touchmove', onDrag, { passive: false });
            document.addEventListener('touchend', stopDrag);
        };

        // Pendant le drag, fait défiler le conteneur
        const onDrag = (e: MouseEvent | TouchEvent) => {
            if (!isDragging) return;
            e.preventDefault();

            const container = cardsContainer.value;
            const track = trackRef.value;
            if (!container || !track) return;

            const clientX = e instanceof MouseEvent ? e.clientX : e.touches[0].clientX;
            const deltaX = clientX - startX;

            // Convertit le déplacement du curseur en défilement proportionnel
            const trackWidth = track.offsetWidth;
            const maxScrollLeft = container.scrollWidth - container.clientWidth;
            const ratio = maxScrollLeft / (trackWidth * (1 - thumbWidth.value / 100));
            container.scrollLeft = startScrollLeft + deltaX * ratio;
        };

        // Arrête le drag
        const stopDrag = () => {
            if (!isDragging) return;
            isDragging = false;

            document.removeEventListener('mousemove', onDrag);
            document.removeEventListener('mouseup', stopDrag);
            document.removeEventListener('touchmove', onDrag);
            document.removeEventListener('touchend', stopDrag);
        };

        // Clic sur la piste : amène le scroll à l'endroit cliqué
        const handleTrackClick = (e: MouseEvent) => {
            const container = cardsContainer.value;
            const track = trackRef.value;
            if (!container || !track) return;

            const rect = track.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const trackWidth = rect.width;

            // Calcule la nouvelle position de défilement
            const thumbWidthPx = (thumbWidth.value / 100) * trackWidth;
            const maxScrollLeft = container.scrollWidth - container.clientWidth;
            const targetScroll = ((clickX - thumbWidthPx / 2) / (trackWidth - thumbWidthPx)) * maxScrollLeft;

            container.scrollTo({
            left: Math.max(0, Math.min(targetScroll, maxScrollLeft)),
            behavior: 'smooth',
            });
        };

        // Surveillance du scroll natif pour synchroniser la scrollbar
        onMounted(() => {
            const container = cardsContainer.value;
            if (container) {
            container.addEventListener('scroll', updateScrollbar);
            updateScrollbar(); // initialisation
            }
        });

        return {
            cardsContainer,
            trackRef,
            thumbWidth,
            thumbLeft,
            showScrollbar,
            startDrag,
            handleTrackClick,
            updateScrollbar,
        };
        }
}
</script>

<style scoped>
@media (min-width: 768px) {
    /* 1. On met l'image principale et les infos produit côte à côte */
    .product-detail-layout {
        flex-direction: row;
        align-items: flex-start;
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    /* 2. On réorganise les images (miniatures à gauche, principale à droite) */
    .pic-detail-layout {
        flex-direction: row-reverse; 
        align-items: flex-start;
        width: 50%; /* La moitié de l'écran pour les images */
    }

    /* 3. L'image principale s'adapte à l'espace disponible */
    .main-pic {
        flex: 1;
        margin-bottom: 0;
    }

    /* 4. LE POINT CLÉ : Les miniatures passent en colonne */
    .cards-layout {
        flex-direction: column;
        overflow-y: auto; /* Active le scroll vertical si besoin */
        overflow-x: hidden;
        height: 100%;
        max-height: 500px; /* À ajuster selon la taille de ton image principale */
        padding: 0;
        gap: 1rem;
    }

    /* 5. Ajustement de la taille des miniatures pour la colonne */
    .second-pic {
        width: 100px; 
        margin-bottom: 0;
    }

    /* 6. On cache la barre de scroll horizontale customisée sur desktop */
    .custom-scrollbar-container {
        display: none;
    }

    /* 7. Ajustement du conteneur des détails du produit */
    .product-detail {
        width: 50%;
        padding-left: 2rem;
    }
}
</style>