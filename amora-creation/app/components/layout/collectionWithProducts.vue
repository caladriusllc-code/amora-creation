<template>
  <section class="collection-detail-section w-full">
    <div
      v-if="productStore.collectionProductsLoading"
      class="status-state loading-state"
      role="status"
      aria-live="polite"
    >
      <div class="spinner"></div>
      <p>Chargement de la collection...</p>
    </div>

    <div
      v-else-if="productStore.collectionProductsError"
      class="status-state error-state"
      role="alert"
    >
      <p>{{ productStore.collectionProductsError }}</p>
    </div>

    <div v-else-if="productStore.collectionWithProducts" class="collection-container">
      <header class="section-header">
        <h2 class="section-title">{{ productStore.collectionWithProducts.name }}</h2>
        <p class="section-subtitle">
          {{ productStore.collectionWithProducts.description || 'Découvrez tous les articles de cette collection.' }}
        </p>
      </header>

      <div
        v-if="productStore.collectionWithProducts.products.length === 0"
        class="empty-state"
      >
        <p>Aucun produit disponible dans cette collection pour le moment.</p>
      </div>

      <div v-else class="products-grid">
        <ProductCards
          v-for="product in productStore.collectionWithProducts.products"
          :key="product.id"
          class="reveal-item"
          :image="getProductImage(product)"
          :name="product.name"
          :price="product.price"
          :base-price="product.price"
          :discount-price="product.discount_price"
          :sale="!!product.discount_price"
          :isLoading="loadingProductIds.has(product.id)"
          @addToCart="addToCart(product.id)"
          @goToProductDetail="goToProductDetail(product.slug)"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRuntimeConfig } from '#app'

import { useProductStore } from '../../stores/productStore'
import { useCartStore } from '~/stores/cartStore'
import ProductCards from '../cards/productCards.vue'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const cartStore = useCartStore()
const runtimeConfig = useRuntimeConfig()
const apiBaseUrl = (runtimeConfig.public.apiBase as string) || 'http://localhost:8000'
const loadingProductIds = ref(new Set<number | string>())

const collectionSlug = computed(() => String(route.params.slug ?? ''))

onMounted(async () => {
  if (!productStore.products.length) {
    await productStore.fetchProducts()
  }

  if (collectionSlug.value) {
    await productStore.fetchCollectionWithProducts(collectionSlug.value)
  }
})

watch(
  () => route.params.slug,
  async (slug) => {
    if (!slug) return

    if (!productStore.products.length) {
      await productStore.fetchProducts()
    }

    await productStore.fetchCollectionWithProducts(String(slug))
  }
)

const goToProductDetail = (slug: string) => {
  router.push(`/product/${slug}`)
}

const addToCart = async (productId: number | string) => {
  const nextLoadingIds = new Set(loadingProductIds.value)
  nextLoadingIds.add(productId)
  loadingProductIds.value = nextLoadingIds

  try {
    await cartStore.addToCart(productId)
  } catch (error) {
    console.error("Erreur lors de l'ajout au panier", error)
  } finally {
    const nextLoadingIdsAfter = new Set(loadingProductIds.value)
    nextLoadingIdsAfter.delete(productId)
    loadingProductIds.value = nextLoadingIdsAfter
  }
}

const normalizeImageUrl = (url?: string): string => {
  if (!url) return ''
  if (/^(http|https|data):/.test(url)) {
    return url
  }
  if (url.startsWith('/')) {
    return `${apiBaseUrl.replace(/\/$/, '')}${url}`
  }
  return url
}

const getProductImage = (product: any): string => {
  const directImage = product?.image
  const firstImage = Array.isArray(product?.images)
    ? product.images[0]?.image || product.images[0]
    : typeof product?.images === 'string'
      ? product.images
      : ''

  const imageUrl = normalizeImageUrl(directImage || firstImage)
  return imageUrl || getPlaceholderImage(product?.name || 'fashion')
}

const getPlaceholderImage = (name: string): string => {
  const encoded = encodeURIComponent(name || 'fashion')
  return `https://images.unsplash.com/featured/?fashion,${encoded}&w=600&q=80`
}
</script>

<style scoped>
.collection-detail-section {
  --bg-section: #f9fafb;
  --text-main: #111827;
  --text-muted: #6b7280;
  --error-color: #ef4444;
  --spinner-color: #111827;
  --spinner-track: #e5e7eb;
  --spacing-base: 1rem;
  --section-padding: 8rem 1rem 1rem 1rem;
  --max-width: 1200px;
  --radius-lg: 16px;

  padding: var(--section-padding);
  background-color: var(--bg-section);
  min-height: 100vh;
}

.collection-container {
  max-width: var(--max-width);
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: calc(var(--spacing-base) * 4);
}

.section-title {
  font-size: clamp(2rem, 4vw, 2.5rem);
  font-weight: 500;
  color: var(--text-main);
  margin-bottom: var(--spacing-base);
  letter-spacing: -0.02em;
}

.section-subtitle {
  color: var(--text-muted);
  font-size: 1.125rem;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.status-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 40vh;
  text-align: center;
  color: var(--text-muted);
  font-size: 1.125rem;
}

.error-state {
  color: var(--error-color);
}

.empty-state {
  text-align: center;
  padding: calc(var(--spacing-base) * 4) calc(var(--spacing-base) * 2);
  color: var(--text-muted);
  background: #ffffff;
  border-radius: var(--radius-lg);
  border: 1px dashed var(--spinner-track);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--spinner-track);
  border-top-color: var(--spinner-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: var(--spacing-base);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: calc(var(--spacing-base) * 2);
  justify-items: center;
}

.products-grid :deep(.pro-card) {
  width: 100%;
  max-width: 300px;
}
</style>
