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
                    <img src="../../assets/fashion/BCO.552ee5f9-0533-44b6-b203-54968fcd8218.png" alt="">
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

        <div class="info-detail-layout">
            <div class="product-detail">
                <h2 class="product-name">Robe d'été Élégance</h2>
                <p class="product-description">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                    Quisquam, quod. Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                    Quisquam, quod.
                </p>
                <div class="buy-section">
                    <p class="product-price">12 000 FCFA</p>
                </div>
                <shopButton @click="$emit('addToCart')"/>
            </div>

            <productSizes/>

            <productColors/>
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
import shopButton from '../buttons/shopButton.vue'

export default {
    components:{
        productGrid,
        productCategory,
        cartButton,
        productSizes,
        productColors,
        shopButton
    },
    emits: ['addToCart'],
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

            const clientX = e instanceof MouseEvent ? e.clientX : e.touches[0].clientX;
            startX = clientX;
            startScrollLeft = container.scrollLeft;

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

        // Clic sur la piste
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

        onMounted(() => {
            const container = cardsContainer.value;
            if (container) {
            container.addEventListener('scroll', updateScrollbar);
            updateScrollbar(); 
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
        padding-top: 4rem;
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