<template>
  <section class="category-detail-section w-full">
    <!-- Le composant est maintenant en PascalCase (Vue Style Guide) -->
    <CategoryList
      :categories="categories"
      :activeCategory="activeCategory"
      @update:activeCategory="setActive"
    />
    <!-- État : Chargement -->
    <div
      v-if="productStore.categoryProductsLoading"
      class="status-state loading-state"
      role="status"
      aria-live="polite"
    >
      <div class="spinner"></div>
      <p>Chargement de la collection...</p>
    </div>

    <!-- État : Erreur -->
    <div
      v-else-if="productStore.categoryProductsError"
      class="status-state error-state"
      role="alert"
    >
      <p>⚠️ {{ productStore.categoryProductsError }}</p>
    </div>

    <!-- État : Succès -->
    <div v-else-if="productStore.categoryWithProducts" class="category-container">

      <header class="section-header">
        <h2 class="section-title">{{ productStore.categoryWithProducts.name }}</h2>
        <p class="section-subtitle">
          {{ productStore.categoryWithProducts.description || 'Découvrez tous les articles de cette catégorie.' }}
        </p>
      </header>

      <!-- État : Vide -->
      <div
        v-if="productStore.categoryWithProducts.products.length === 0"
        class="empty-state"
      >
        <p>Aucun produit disponible dans cette catégorie pour le moment.</p>
      </div>

      <!-- Grille de produits -->
      <div v-else class="products-grid">
        <ProductCards
          v-for="product in productStore.categoryWithProducts.products"
          :key="product.id"
          class="reveal-item"
          :image="getProductImage(product)"
          :name="product.name"
          :price="product.price"
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
// 1. Imports
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRuntimeConfig } from '#app'

// Stores
import { useProductStore } from '../../stores/productStore'
import { useCartStore } from '~/stores/cartStore'

// Composants
import CategoryList from '../tools/categoryList.vue'
import ProductCards from '../cards/productCards.vue'

// 2. Initialisation
const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const cartStore = useCartStore()
const runtimeConfig = useRuntimeConfig()
const apiBaseUrl = (runtimeConfig.public.apiBase as string) || 'http://localhost:8000'

// 3. États réactifs
const loadingProductIds = ref(new Set<number | string>())

// NOUVEAU : État de la catégorie active (initialisé avec l'URL ou une valeur par défaut)
const activeCategory = ref<string | number>((route.params.id as string) || 'robes')

// NOUVEAU : Liste des catégories à envoyer à l'enfant.
// Note : Si tu as ces catégories dans ton store, tu peux faire `const categories = computed(() => productStore.categories)`
const categories = computed(() => productStore.categories)

// 4. Cycle de vie
onMounted(async () => {
  // Charger les catégories si le store est vide
  if (productStore.categories.length === 0) {
    await productStore.fetchCategories()
  }
  
  const routeId = route.params.id as string
  if (routeId) {
    activeCategory.value = routeId // S'assure que le bouton actif correspond à l'URL
    await productStore.fetchCategoryWithProducts(routeId)
  }
})

// 5. Méthodes (Actions)

// NOUVEAU : Gère le clic sur une catégorie depuis l'enfant
const setActive = async (categoryId: string | number) => {
  if (activeCategory.value === categoryId) return // Évite de recharger si on clique sur la même catégorie

  activeCategory.value = categoryId

  // Met à jour l'URL silencieusement pour que l'utilisateur puisse partager le lien
  // (Assure-toi que la structure de l'URL correspond à ton routeur, ex: /categories/robes)
  router.push({ params: { id: String(categoryId) } })

  // Déclenche le chargement des nouveaux produits dans le store
  await productStore.fetchCategoryWithProducts(categoryId)
}

const goToProductDetail = (slug: string) => {
  router.push(`/produits/${slug}`)
}

const addToCart = async (productId: number | string) => {
  const nextLoadingIds = new Set(loadingProductIds.value)
  nextLoadingIds.add(productId)
  loadingProductIds.value = nextLoadingIds
  try {
    await cartStore.addToCart(productId)
    console.log(`Produit ${productId} ajouté au panier !`)
  } catch (error) {
    console.error("Erreur lors de l'ajout au panier", error)
  } finally {
    const nextLoadingIdsAfter = new Set(loadingProductIds.value);
    nextLoadingIdsAfter.delete(productId);
    loadingProductIds.value = nextLoadingIdsAfter;
  }
}

// 6. Méthodes (Utilitaires de formatage)
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
/* =========================================
   VARIABLES CSS (Thème de la section)
   ========================================= */
.category-detail-section {
  /* Couleurs */
  --bg-section: #f9fafb;
  --text-main: #111827;
  --text-muted: #6b7280;
  --error-color: #ef4444;
  --spinner-color: #111827;
  --spinner-track: #e5e7eb;

  /* Espacements et Dimensions */
  --spacing-base: 1rem;
  --section-padding: 8rem 1rem 1rem 1rem;
  --max-width: 1200px;
  --radius-lg: 16px;

  padding: var(--section-padding);
  background-color: var(--bg-section);
  min-height: 100vh;
}

.category-container {
  max-width: var(--max-width);
  margin: 0 auto;
}

/* =========================================
   EN-TÊTE DE SECTION
   ========================================= */
.section-header {
  text-align: center;
  margin-bottom: calc(var(--spacing-base) * 4);
}

.section-title {
  font-size: clamp(2rem, 4vw, 2.5rem); /* Taille responsive fluide */
  font-weight: 700;
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

/* =========================================
   ÉTATS (CHARGEMENT, ERREUR, VIDE)
   ========================================= */
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

/* Spinner d'attente */
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

/* =========================================
   GRILLE DES PRODUITS
   ========================================= */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: calc(var(--spacing-base) * 2);
  justify-items: center;
}

/* On cible le composant enfant sans rompre le scope */
.products-grid :deep(.pro-card) {
  width: 100%;
  max-width: 300px;
}
</style>
