import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useNuxtApp } from '#app'

export interface Category {
  id?: number,
  name: string,
  slug: string,
  description?: string,
  image?: string
}

export const useProductStore = defineStore('product', () => {
  // 1. Récupérer ton instance API personnalisée
  const { $api } = useNuxtApp()

  // ==========================
  // 📦 STATE (État)
  // ==========================
  const products = ref([])
  const currentProduct = ref(null)
  const categories = ref<Category[]>([])
  const collections = ref([])
  
  // États de l'interface utilisateur
  const isLoading = ref(false)
  const error = ref(null)
  const categoriesLoading = ref(false)
  const categoriesError = ref(null)
  const collectionsLoading = ref(false)
  const collectionsError = ref(null)

  // ==========================
  // ⚙️ ACTIONS (Méthodes)
  // ==========================

  // Récupérer tous les produits
  const fetchProducts = async () => {
    isLoading.value = true
    error.value = null
    try {
      // Rappel : dans urls.py tu avais mis path('product/', ...)
      const response = await $api('/product/products/')
      
      // Django REST Framework renvoie souvent { count, next, previous, results: [...] } 
      // si la pagination est activée. Sinon, c'est directement le tableau.
      products.value = response.results ? response.results : response
    } catch (err) {
      error.value = "Impossible de charger les produits d'Amora création."
      console.error("Erreur fetchProducts:", err)
    } finally {
      isLoading.value = false
    }
  }

  // Récupérer un seul produit via son slug (pour la page détail)
  const fetchProductBySlug = async (slug) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await $api(`/product/products/${slug}/`)
      currentProduct.value = response
    } catch (err) {
      error.value = "Ce produit est introuvable."
      console.error("Erreur fetchProductBySlug:", err)
    } finally {
      isLoading.value = false
    }
  }

  // Récupérer les catégories (pour ton menu ou tes filtres)
  const fetchCategories = async () => {
    categoriesLoading.value = true
    categoriesError.value = null
    try {
      const response = await $api('/product/categories/')
      categories.value = response.results ? response.results : response
    } catch (err) {
      categoriesError.value = "Impossible de charger les catégories."
      console.error("Erreur fetchCategories:", err)
    } finally {
      categoriesLoading.value = false
    }
  }

  // Récupérer les collections actives
  const fetchCollections = async () => {
    collectionsLoading.value = true
    collectionsError.value = null
    try {
      const response = await $api('/product/collections/')
      collections.value = response.results ? response.results : response
    } catch (err) {
      collectionsError.value = "Impossible de charger les collections."
      console.error("Erreur fetchCollections:", err)
    } finally {
      collectionsLoading.value = false
    }
  }

  // ==========================
  // 🔍 GETTERS (Propriétés calculées)
  // ==========================
  
  // Exemple de getter : récupérer les produits en stock uniquement
  const inStockProducts = computed(() => {
    return products.value.filter(p => p.is_in_stock)
  })

  // ==========================
  // 🚀 RETOUR
  // ==========================
  return {
    // State
    products,
    currentProduct,
    categories,
    collections,
    isLoading,
    error,
    categoriesLoading,
    categoriesError,
    collectionsLoading,
    collectionsError,
    // Actions
    fetchProducts,
    fetchProductBySlug,
    fetchCategories,
    fetchCollections,
    // Getters
    inStockProducts
  }
})