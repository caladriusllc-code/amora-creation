<template>
  <section class="category-detail-section w-full">
    <div v-if="productStore.categoryProductsLoading" class="status-state loading-state">
      <div class="spinner"></div>
      <p>Chargement de la collection...</p>
    </div>

    <div v-else-if="productStore.categoryProductsError" class="status-state error-state">
      <p>⚠️ {{ productStore.categoryProductsError }}</p>
    </div>

    <div v-else-if="productStore.categoryWithProducts" class="category-container">
      
      <div class="section-header">
        <h2 class="section-title">{{ productStore.categoryWithProducts.name }}</h2>
        <p class="section-subtitle">{{ productStore.categoryWithProducts.description || 'Découvrez tous les articles de cette catégorie.' }}</p>
      </div>

      <div v-if="productStore.categoryWithProducts.products.length === 0" class="empty-state">
        <p>Aucun produit disponible dans cette catégorie pour le moment.</p>
      </div>

      <div v-else class="products-grid">
        <ProductCards
            v-for="product in productStore.categoryWithProducts.products"
            :key="product.id"
            class="reveal-item"
            v-scroll-reveal
            :image="getProductImage(product)"
            :name="product.name"
            :price="product.price"
            :sale="product.discount_price ? true : false"
            :isLoading="loadingProductIds.has(product.id)"
            @addToCart="addToCart(product.id)"
            @goToProductDetail="goToProductDetail(product.slug)"
        />
      </div>

    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '../../stores/productStore'
// Optionnel: Importe ton store panier si tu l'utilises ici pour ajouter l'article
// import { useCartStore } from '../../stores/cartStore'

import ProductCards from '../cards/productCards.vue'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const runtimeConfig = useRuntimeConfig()
const apiBaseUrl = (runtimeConfig.public.apiBase as string) || 'http://localhost:8000'
// const cartStore = useCartStore()

// Un Set pour suivre de manière réactive quels produits sont en cours d'ajout au panier
const loadingProductIds = ref(new Set<number | string>())

onMounted(async () => {
  const routeId = route.params.id as string
  if (routeId) {
    await productStore.fetchCategoryWithProducts(routeId)
  }
})

// Fonction pour aller sur la page détail du produit
const goToProductDetail = (slug: string) => {
  // ⚠️ Assure-toi que la route vers les détails correspond à ce nom dans ton router
  router.push(`/produits/${slug}`) 
}

// Fonction pour ajouter au panier
const addToCart = async (productId: number | string) => {
  // On active le chargement pour CE produit spécifique
  loadingProductIds.value.add(productId)
  
  try {
    // Appel de ton store cart (à décommenter quand tu es prêt)
    // await cartStore.add(productId)
    
    // Simulation du temps de réseau pour voir l'effet de chargement (à retirer ensuite)
    await new Promise(resolve => setTimeout(resolve, 800))
    console.log(`Produit ${productId} ajouté au panier !`)
  } catch (error) {
    console.error("Erreur lors de l'ajout au panier", error)
  } finally {
    // On désactive le chargement une fois fini
    loadingProductIds.value.delete(productId)
  }
}

const normalizeImageUrl = (url?: string) => {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
    return url
  }
  if (url.startsWith('/')) {
    return `${apiBaseUrl.replace(/\/$/, '')}${url}`
  }
  return url
}

const getProductImage = (product: any) => {
  const directImage = product?.image
  const firstImage = Array.isArray(product?.images)
    ? product.images[0]?.image || product.images[0]
    : typeof product?.images === 'string'
      ? product.images
      : ''

  const imageUrl = normalizeImageUrl(directImage || firstImage)
  return imageUrl || getPlaceholderImage(product?.name || 'fashion')
}

// Fonction pour générer une image par défaut (fallback)
const getPlaceholderImage = (name: string) => {
  const encoded = encodeURIComponent(name || 'fashion')
  return `https://images.unsplash.com/featured/?fashion,${encoded}&w=600&q=80`
}
</script>

<style scoped>
/* =========================================
   VARIABLES & CONTENEUR GLOBAL
   ========================================= */
.category-detail-section {
  padding: 4rem 1.5rem;
  background-color: #f9fafb;
  min-height: 100vh;
}

.category-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* =========================================
   EN-TÊTE DE SECTION
   ========================================= */
.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 1rem;
  letter-spacing: -0.02em;
}

.section-subtitle {
  color: #6b7280;
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
  color: #4b5563;
  font-size: 1.125rem;
}

.error-state { color: #ef4444; }
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6b7280;
  background: white;
  border-radius: 16px;
  border: 1px dashed #d1d5db;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top-color: #111827;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* =========================================
   GRILLE DES PRODUITS
   ========================================= */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2rem;
  /* Optionnel : centre les cartes dans leur colonne si on est sur un grand écran */
  justify-items: center; 
}

/* On force l'enfant (qui a une width fixe de 280px par défaut)
  à prendre 100% de sa colonne pour rester parfaitement responsive
*/
.products-grid :deep(.pro-card) {
  width: 100%;
  max-width: 300px;
}
</style>