<template>
  <section class="product-section" id="grid-products">
    <div class="section-header">
      <h2 class="section-title">{{ title }}</h2>
      <p class="section-subtitle">{{ subtitle }}</p>
    </div>
    
    <div v-if="productStore.isLoading" class="loading-state">
      <skeleton />
    </div>

    <div v-else-if="productStore.error" class="error-state">
      <p>{{ productStore.error }}</p>
    </div>

    <div v-else class="cards-layout" ref="cardsContainer" @scroll="updateScrollbar">
      <ProductCards
        v-for="product in formattedProducts"
        :key="product.id"
        class="reveal-item"
        v-scroll-reveal
        :image="product.image"
        :name="product.name"
        :price="product.price"
        :base-price="product.basePrice"
        :discount-price="product.discountPrice"
        :sale="product.discount_percentage ? `-${product.discount_percentage}%` : false"
        :isLoading="loadingProductIds.has(product.id)"
        @addToCart="addToCart(product.id)"
        @goToProductDetail="goToProductDetail(product.slug)"
      />

      <moreProductButton 
        v-if="showDiscoverMore" 
        type="button" 
        aria-label="Découvrir plus de produits"
        @click="goToDiscoverMore"
      />
    </div>

    <div v-show="showScrollbar && !productStore.isLoading" class="custom-scrollbar-container">
      <div class="scrollbar-track" ref="trackRef" @click="handleTrackClick">
        <div 
          class="scrollbar-thumb" 
          :style="{ width: `${thumbWidth}%`, left: `${thumbLeft}%` }"
          @mousedown.prevent="startDrag"
          @touchstart="startDrag"
        ></div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useProductStore } from '../../stores/productStore';
import { useCartStore } from '../../stores/cartStore';

import ProductCards from '../cards/ProductCards.vue'; 
import skeleton from '../tools/skeleton.vue';
import moreProductButton from '../buttons/moreProductButton.vue';

// Définition des props
interface Props {
  title?: string;
  subtitle?: string;
  collectionId?: number | string;
  maxProducts?: number;
  showDiscoverMore?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  title: "Produits de la collection",
  subtitle: "Découvrez tous les produits de la collection",
  collectionId: undefined,
  maxProducts: undefined,
  showDiscoverMore: false,
});

// Initialisation des stores et router
const productStore = useProductStore();
const cartStore = useCartStore();
const router = useRouter();
const loadingProductIds = ref<Set<string | number>>(new Set());

// ------------------------------------------------------------------
// ANIMATION AU SCROLL (Nouvelle logique)
// ------------------------------------------------------------------
let delayCounter = 0;
let delayTimer: ReturnType<typeof setTimeout> | null = null;

// Directive Vue personnalisée
const vScrollReveal = {
  mounted: (el: HTMLElement) => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Applique un délai incrémental pour l'effet en cascade
            setTimeout(() => {
              entry.target.classList.add('is-visible');
            }, delayCounter * 120); // 120ms entre chaque carte

            delayCounter++;

            // Réinitialise le compteur quand la "vague" d'apparition est terminée
            if (delayTimer) clearTimeout(delayTimer);
            delayTimer = setTimeout(() => {
              delayCounter = 0;
            }, 50);

            // Arrête d'observer l'élément une fois apparu (pour ne pas rejouer l'animation)
            observer.unobserve(entry.target);
          }
        });
      },
      { 
        threshold: 0.1 // L'animation se déclenche quand 10% de la carte est visible
      }
    );
    observer.observe(el);
  }
};

// ------------------------------------------------------------------
// FORMATAGE DES DONNÉES
// ------------------------------------------------------------------
const formattedProducts = computed(() => {
  let productsToShow = productStore.products;
  
  if (props.collectionId) {
    productsToShow = productsToShow.filter(p => {
      const productCollectionId = p.collection?.id || p.collection;
      return productCollectionId === props.collectionId;
    });
  }

  const limitedProducts = props.maxProducts
    ? productsToShow.slice(0, props.maxProducts)
    : productsToShow;

  return limitedProducts.map(p => {
    let imageUrl = 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80';
    if (p.images && p.images.length > 0) {
      const mainImg = p.images.find(img => img.is_main);
      imageUrl = mainImg ? mainImg.image : p.images[0].image;
    }

    return {
      id: p.id,
      slug: p.slug,
      name: p.name,
      basePrice: Number(p.price),
      price: p.discount_price ? Number(p.discount_price) : Number(p.price),
      discountPrice: p.discount_price ? Number(p.discount_price) : null,
      image: imageUrl,
      sale: p.discount_price !== null && p.discount_price !== undefined
    }
  });
});

// ------------------------------------------------------------------
// LOGIQUE DE LA SCROLLBAR
// ------------------------------------------------------------------
const cardsContainer = ref<HTMLElement | null>(null);
const trackRef = ref<HTMLElement | null>(null);

const thumbWidth = ref(0);
const thumbLeft = ref(0);
const showScrollbar = ref(false);

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

const handleTrackClick = (e: MouseEvent) => {
  const track = trackRef.value;
  const container = cardsContainer.value;
  if (!track || !container) return;
  
  const rect = track.getBoundingClientRect();
  const clickX = e.clientX - rect.left;
  const clickRatio = clickX / rect.width;
  
  const maxScrollLeft = container.scrollWidth - container.clientWidth;
  let targetScrollLeft = (clickRatio * container.scrollWidth) - (container.clientWidth / 2);
  targetScrollLeft = Math.max(0, Math.min(maxScrollLeft, targetScrollLeft));
  
  container.scrollTo({
    left: targetScrollLeft,
    behavior: 'smooth'
  });
};

let isDragging = false;
let startX = 0;
let startScrollLeft = 0;

const handleDrag = (e: MouseEvent | TouchEvent) => {
  if (!isDragging || !cardsContainer.value || !trackRef.value) return;
  
  const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
  const deltaX = clientX - startX;
  
  const trackWidth = trackRef.value.clientWidth;
  const container = cardsContainer.value;
  const maxScrollLeft = container.scrollWidth - container.clientWidth;
  
  const thumbWidthPx = (thumbWidth.value / 100) * trackWidth;
  const thumbScrollRange = trackWidth - thumbWidthPx;
  
  if (thumbScrollRange <= 0) return;
  
  const ratio = deltaX / thumbScrollRange;
  container.scrollLeft = startScrollLeft + ratio * maxScrollLeft;
};

const stopDrag = () => {
  isDragging = false;
  window.removeEventListener('mousemove', handleDrag);
  window.removeEventListener('touchmove', handleDrag);
  window.removeEventListener('mouseup', stopDrag);
  window.removeEventListener('touchend', stopDrag);
};

const startDrag = (e: MouseEvent | TouchEvent) => {
  isDragging = true;
  const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
  startX = clientX;
  if (cardsContainer.value) {
    startScrollLeft = cardsContainer.value.scrollLeft;
  }
  
  window.addEventListener('mousemove', handleDrag);
  window.addEventListener('touchmove', handleDrag, { passive: true });
  window.addEventListener('mouseup', stopDrag);
  window.addEventListener('touchend', stopDrag);
};

// ------------------------------------------------------------------
// ACTIONS PRODUITS
// ------------------------------------------------------------------
async function addToCart(id: string | number) {
  const nextLoadingIds = new Set(loadingProductIds.value);
  nextLoadingIds.add(id);
  loadingProductIds.value = nextLoadingIds;

  try {
    await cartStore.addToCart(id, 1);
  } catch (error){
    console.error("Erreur lors de la récupération du panier:", error);
  } finally {
    const nextLoadingIdsAfter = new Set(loadingProductIds.value);
    nextLoadingIdsAfter.delete(id);
    loadingProductIds.value = nextLoadingIdsAfter;
  }
}

function goToProductDetail(slug: string) {
  router.push(`/product/${slug}`);
}

function goToDiscoverMore() {
  router.push('/tendances');
}

// Lifecycle hooks
let resizeObserver: ResizeObserver | null = null;

onMounted(async () => {
  await productStore.fetchProducts();

  updateScrollbar();
  window.addEventListener('resize', updateScrollbar);
  
  if (typeof ResizeObserver !== 'undefined' && cardsContainer.value) {
    resizeObserver = new ResizeObserver(updateScrollbar);
    resizeObserver.observe(cardsContainer.value);
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', updateScrollbar);
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
  stopDrag();
});
</script>

<style scoped>
/* ------------------------------------------------------------------ */
/* 🎭 STYLES D'ANIMATION DES CARTES                                   */
/* ------------------------------------------------------------------ */
.reveal-item {
  opacity: 0;
  /* La carte est légèrement poussée vers la droite/le bas avant d'apparaître */
  transform: translateY(20px) scale(0.95); 
  transition: opacity 0.6s cubic-bezier(0.25, 0.8, 0.25, 1), 
              transform 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.reveal-item.is-visible {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* ------------------------------------------------------------------ */
/* STYLES EXISTANTS                                                   */
/* ------------------------------------------------------------------ */
.product-section {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px 8px;
  /*min-height: 100vh;*/
  overflow-x: hidden;
}

.section-header {
  display: flex;
  flex-direction: column;
  gap:1rem;
  margin-bottom: 24px;
}

.section-title {
  font-size: 30px;
  font-weight: 700;
  text-transform: uppercase;
  margin: 0;
}

.cards-layout {
  display: flex;
  align-items: center;
  gap: 24px;
  overflow-x: auto;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE/Edge */
}
.cards-layout::-webkit-scrollbar {
  display: none; /* Chrome/Safari */
}

.discover-more-card {
  flex: 0 0 280px;
  min-height: 380px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  border: 1px solid #d1d5db;
  background: #f9fafb;
  color: #111827;
  cursor: pointer;
  font: inherit;
  font-weight: 600;
  transition: background-color 0.2s, border-color 0.2s, transform 0.2s;
}

.discover-more-card:hover,
.discover-more-card:focus-visible {
  border-color: #111827;
  background: #f3f4f6;
  transform: translateY(-4px);
}

.discover-more-icon {
  width: 56px;
  height: 56px;
  display: grid;
  place-items: center;
  border: 1px solid currentColor;
  border-radius: 50%;
  font-size: 32px;
  font-weight: 300;
  line-height: 1;
}

.custom-scrollbar-container {
  width: 100%;
  max-width: 400px;
  margin: 32px auto 0 auto;
  padding: 0 16px;
}

.scrollbar-track {
  width: 100%;
  height: 4px;
  background-color: #e5e7eb;
  border-radius: 9999px;
  position: relative;
  cursor: pointer;
  transition: background-color 0.2s, height 0.2s;
}

.scrollbar-track:hover {
  height: 6px;
  background-color: #d1d5db;
}

.scrollbar-thumb {
  height: 100%;
  background-color: #111827;
  border-radius: 9999px;
  position: absolute;
  top: 0;
  left: 0;
  cursor: grab;
  transition: background-color 0.2s;
}

.scrollbar-thumb:hover {
  background-color: #374151;
}

.scrollbar-thumb:active {
  cursor: grabbing;
  background-color: #000000;
}

@media(min-width:768px){

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40px;
  }

}
</style>