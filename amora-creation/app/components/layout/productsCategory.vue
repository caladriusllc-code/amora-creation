<template>
  <section class="product-section" id="grid-products">
    <div class="section-header">
      <h2 class="section-title">Categorie de produits</h2>
      <p class="section-subtitle">Découvrez toutes nos catégories de vêtements</p>
    </div>
    
    <div v-if="productStore.categoriesLoading" class="loading-state">
      <p>Chargement des catégories...</p>
    </div>

    <div v-else-if="productStore.categoriesError" class="error-state">
      <p>{{ productStore.categoriesError }}</p>
    </div>

    <div v-else class="cards-layout" ref="cardsContainer" @scroll="updateScrollbar">
      <productsCategory
        v-for="category in productStore.categories"
        :key="category.id || category.slug"
        :image="getCategoryImage(category)"
        :title="category.name"
      />
    </div>

    <!-- Custom Scrollbar -->
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
  </section>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useProductStore } from '../../stores/productStore';
import productsCategory from '../cards/categoryCards.vue'

export default {
  components:{
    productsCategory,
  },
  setup() {
    const productStore = useProductStore()

    // Refs for scroll elements
    const cardsContainer = ref<HTMLElement | null>(null);
    const trackRef = ref<HTMLElement | null>(null);
    
    // Scrollbar state
    const thumbWidth = ref(0);
    const thumbLeft = ref(0);
    const showScrollbar = ref(false);

    // Update scrollbar dimensions and positioning
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
      const calculatedWidth = Math.max(10, Math.min(100, visibleRatio * 100)); // Clamp between 10% and 100%
      thumbWidth.value = calculatedWidth;
      
      const maxScrollLeft = scrollWidth - clientWidth;
      const progress = maxScrollLeft > 0 ? scrollLeft / maxScrollLeft : 0;
      thumbLeft.value = progress * (100 - calculatedWidth);
    };

    // Navigation buttons handlers
    const scrollPrev = () => {
      const container = cardsContainer.value;
      if (!container) return;
      const scrollAmount = container.clientWidth * 0.75;
      container.scrollBy({
        left: -scrollAmount,
        behavior: 'smooth'
      });
    };

    const scrollNext = () => {
      const container = cardsContainer.value;
      if (!container) return;
      const scrollAmount = container.clientWidth * 0.75;
      container.scrollBy({
        left: scrollAmount,
        behavior: 'smooth'
      });
    };

    // Track click handler
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

    // Drag-and-drop thumb handlers
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

    // Lifecycle hooks
    let resizeObserver: ResizeObserver | null = null;
    
    onMounted(async () => {
      await productStore.fetchCategories()
      await nextTick()
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

    const getCategoryImage = (category: any) => {
      if (category.image) {
        return category.image
      }
      if (category.slug) {
        return `https://images.unsplash.com/featured/?fashion,${encodeURIComponent(category.slug)}&w=900&q=80`
      }
      return 'https://images.unsplash.com/featured/?fashion&w=900&q=80'
    }

    return { 
      productStore,
      cardsContainer,
      trackRef,
      thumbWidth,
      thumbLeft,
      showScrollbar,
      updateScrollbar,
      scrollPrev,
      scrollNext,
      handleTrackClick,
      startDrag,
      getCategoryImage
    };
  }
}
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