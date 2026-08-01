<template>
  <section class="product-section" id="grid-products">
    <div class="section-header">
      <h2 class="section-title">{{ title }}</h2>
      <p class="section-subtitle">{{ subtitle }}</p>
    </div>
    
    <div v-if="productStore.isLoading" class="loading-state">
      <p>Chargement des collections Amora...</p>
    </div>

    <div v-else-if="productStore.error" class="error-state">
      <p>{{ productStore.error }}</p>
    </div>

    <div v-else class="cards-layout" ref="cardsContainer" @scroll="updateScrollbar">
      <ProductCards
        v-for="product in formattedProducts"
        :key="product.id"
        :image="product.image"
        :name="product.name"
        :price="product.price"
        :sale="product.sale"
        @addToCart="addToCart(product.id)"
        @goToProductDetail="goToProductDetail(product.slug)"
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
import ProductCards from '../cards/ProductCards.vue'; 
import { useRouter } from 'vue-router';
// 🛠️ 1. On importe ton Store Pinia
import { useProductStore } from '../../stores/productStore';
import { useCartStore } from '../../stores/cartStore';

// Définition des props (On enlève 'products' car c'est le store qui gère ça maintenant)
interface Props {
  title?: string;
  subtitle?: string;
  collectionId?: number | string;
}

const props = withDefaults(defineProps<Props>(), {
  title: "Produits de la collection",
  subtitle: "Découvrez tous les produits de la collection",
  collectionId: undefined,
});

// 🛠️ 2. On initialise le store et le router
const productStore = useProductStore();
const cartStore = useCartStore();
const router = useRouter();

// 🛠️ 3. On formate les données de Django pour qu'elles collent parfaitement à ton design
// 🛠️ 3. On filtre et on formate les données de Django
const formattedProducts = computed(() => {
  
  // ✨ ÉTAPE A : On filtre les produits si un collectionId a été passé
  let productsToShow = productStore.products;
  
  if (props.collectionId) {
    productsToShow = productsToShow.filter(p => {
      // Selon comment ton backend Django envoie la donnée, 
      // p.collection peut être directement un ID (ex: 2) ou un objet (ex: { id: 2, name: '...' })
      const productCollectionId = p.collection?.id || p.collection;
      return productCollectionId === props.collectionId;
    });
  }

  // ✨ ÉTAPE B : On formate les produits filtrés (ton code précédent intact)
  return productsToShow.map(p => {
    let imageUrl = 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80';
    if (p.images && p.images.length > 0) {
      const mainImg = p.images.find(img => img.is_main);
      imageUrl = mainImg ? mainImg.image : p.images[0].image;
    }

    return {
      id: p.id,
      slug: p.slug,
      name: p.name,
      price: p.discount_price ? parseFloat(p.discount_price) : parseFloat(p.price),
      image: imageUrl,
      sale: p.discount_price !== null && p.discount_price !== undefined
    }
  });
});

// ------------------------------------------------------------------
// LOGIQUE DE LA SCROLLBAR (inchangée)
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

  try {
    await cartStore.addToCart(id, 1);
  } catch (error){
    console.error("Erreur lors de la récupération du panier:", error);
  }
  console.log(`Produit ${id} ajouté au panier!`);
  // Plus tard, tu pourras appeler ton cartStore ici
}

function goToProductDetail(slug: string) {
  // On utilise le slug généré par Django pour faire une belle URL SEO-friendly !
  router.push(`/product/${slug}`);
  console.log(`Allons à la page de detail du produit: ${slug}`);
}

// Lifecycle hooks
let resizeObserver: ResizeObserver | null = null;

onMounted(async () => {
  // 🛠️ 4. On demande au store d'aller chercher les produits sur Django
  await productStore.fetchProducts();

  // On met à jour la scrollbar une fois les données chargées
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
.product-section {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 64px 24px;
  overflow-x: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
}

.section-title {
  font-size: 30px;
  font-weight: 700;
  text-transform: uppercase;
  margin: 0;
}

.control-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #e5e7eb;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-btn:hover {
  background: #000;
  color: #fff;
}

.image-wrapper {
  aspect-ratio: 1 / 1;
  position: relative;
  background-color: #f3f3f3;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 16px;
}

.sale-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  background-color: #ef4444;
  color: white;
  font-size: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: bold;
  text-transform: uppercase;
  z-index: 10;
  font-family: 'Inter', sans-serif;
}

/* Custom Scrollbar Styles */
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
</style>