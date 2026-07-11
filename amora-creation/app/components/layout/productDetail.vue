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
                    <img src="../../assets/fashion/BCO.9a51f253-80c6-4638-b350-1cdce66a38ef.png" alt="">
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

            <productSizes/>

            <productColors/>
        </div>
        <div class="product-detail">
            <h2 class="product-name">Robe d'été Élégance</h2>
            <p class="product-description">
                Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                Quisquam, quod. Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                Quisquam, quod.
            </p>
            <p class="product-price">12 000 FCFA</p>
            <cartButton/>
        </div>
    </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import productGrid from '../layout/productGrid.vue';
import productCategory from '../layout/productsCategory.vue'
import cartButton from '../buttons/cartButton.vue'
import productSizes from '../tools/productSizes.vue'
import productColors from '../tools/productColors.vue'
export default {
    components:{
        productGrid,
        productCategory,
        cartButton,
        productSizes,
        productColors
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
/* =========================================
   STYLES MOBILE (Téléphone) - Par défaut
   ========================================= */

/* 1. Conteneur principal limité à la largeur de l'écran */
.product-detail-layout {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-height: 100vh;
}

/* 2. Conteneur des images limité à 100% */
.pic-detail-layout {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 100%;
}

.main-pic img {
    width: 100%;
    height: auto;
    object-fit: cover;
}

.product-detail{
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.product-name {
    font-size: 1.5rem;
    font-weight: 500;
}

/* 3. LE POINT CLÉ MOBILE : Les miniatures côte à côte et scrollables */
.cards-layout {
    display: flex;
    flex-direction: row; /* Aligne les images horizontalement */
    overflow-x: auto; /* Active le défilement horizontal */
    width: 100%;
    gap: 12px; /* Espace entre les images */
    padding: 5px;
    
    /* Masque la barre de défilement par défaut du navigateur 
       pour laisser ta barre personnalisée (custom-scrollbar) faire le travail */
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE/Edge */
}
.cards-layout::-webkit-scrollbar {
    display: none; /* Chrome/Safari/Opera */
}

/* 4. On force les miniatures à garder leur taille */
.second-pic {
    flex-shrink: 0; /* Empêche les images de s'écraser les unes sur les autres */
    width: 45%; /* Largeur de tes miniatures sur mobile */
    height: 220px; /* Hauteur de tes miniatures (à ajuster selon tes photos) */
}

.second-pic img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 8px; /* Un petit bord arrondi chic pour Amora création */
}

/* Styles pour ta barre de défilement personnalisée sur mobile */
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
    background-color: #333; /* Couleur de la barre de progression */
    border-radius: 4px;
    position: absolute;
    top: 0;
}




/* =========================================
   STYLES DESKTOP / LAPTOP (Écrans larges)
   ========================================= */
@media (min-width: 768px) {
    /* ... Ton code existant pour le desktop reste ici sans changement ... */
    .product-detail-layout {
        flex-direction: row;
        align-items: flex-start;
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    .pic-detail-layout {
        flex-direction: row-reverse; 
        align-items: flex-start;
        width: 50%;
    }

    .main-pic {
        flex: 1;
        margin-bottom: 0;
    }

    .cards-layout {
        flex-direction: column;
        overflow-y: auto; 
        overflow-x: hidden;
        height: 100%;
        max-height: 500px; 
        padding: 0;
        gap: 1rem;
    }

    .second-pic {
        width: 100px; 
        margin-bottom: 0;
    }

    .custom-scrollbar-container {
        display: none;
    }

    .product-detail {
        width: 50%;
        padding-left: 2rem;
    }
}
</style>