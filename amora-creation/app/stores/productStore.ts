import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useNuxtApp } from '#app'

// ==========================
// 📚 INTERFACES (Typage)
// ==========================

export interface Category {
  id?: number
  name: string
  slug: string
  description?: string
  image?: string
}

export interface Collection {
  id?: number
  name: string
  slug: string
  description?: string
  image?: string
}

export interface ProductImage {
  id?: number | string
  image: string
  is_main?: boolean
}

export interface Product {
  id?: number | string
  name: string
  slug: string
  description: string
  price: number | string
  discount_price?: number | string | null
  image?: string
  images?: ProductImage[]
  category?: Category
  collection?: Collection | number | string
  is_in_stock?: boolean
}

// Typage générique pour les réponses paginées de Django REST Framework
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const useProductStore = defineStore('product', () => {
  // 1. Récupérer l'instance API personnalisée
  const { $api } = useNuxtApp()

  // ==========================
  // 📦 STATE (État)
  // ==========================
  
  // Données
  const products = ref<Product[]>([])
  const currentProduct = ref<Product | null>(null)
  const categories = ref<Category[]>([])
  const collections = ref<Collection[]>([])
  
  // États de l'interface utilisateur (Chargement)
  const isLoading = ref<boolean>(false)
  const categoriesLoading = ref<boolean>(false)
  const collectionsLoading = ref<boolean>(false)

  // États de l'interface utilisateur (Erreurs)
  const error = ref<string | null>(null)
  const categoriesError = ref<string | null>(null)
  const collectionsError = ref<string | null>(null)

  // ==========================
  // ⚙️ ACTIONS (Méthodes)
  // ==========================

  // Récupérer tous les produits
  const fetchProducts = async () => {
    isLoading.value = true
    error.value = null
    try {
      // Typage explicite du retour de l'API
      const response = await $api<PaginatedResponse<Product> | Product[]>('/product/products/')
      
      products.value = 'results' in response ? response.results : response
    } catch (err: any) {
      error.value = err?.data?.message || "Impossible de charger les produits d'Amora création."
      console.error("Erreur fetchProducts:", err)
    } finally {
      isLoading.value = false
    }
  }

  // Récupérer un seul produit via son slug
  const fetchProductBySlug = async (slug: string) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await $api<Product>(`/product/products/${slug}/`)
      currentProduct.value = response
    } catch (err: any) {
      error.value = err?.data?.message || "Ce produit est introuvable."
      console.error(`Erreur fetchProductBySlug (${slug}):`, err)
    } finally {
      isLoading.value = false
    }
  }

  // Récupérer les catégories
  const fetchCategories = async () => {
    categoriesLoading.value = true
    categoriesError.value = null
    try {
      const response = await $api<PaginatedResponse<Category> | Category[]>('/product/categories/')
      categories.value = 'results' in response ? response.results : response
    } catch (err: any) {
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
      const response = await $api<PaginatedResponse<Collection> | Collection[]>('/product/collections/')
      collections.value = 'results' in response ? response.results : response
    } catch (err: any) {
      collectionsError.value = "Impossible de charger les collections."
      console.error("Erreur fetchCollections:", err)
    } finally {
      collectionsLoading.value = false
    }
  }

  // ==========================
  // 🔍 GETTERS (Propriétés calculées)
  // ==========================
  
  const inStockProducts = computed<Product[]>(() => {
    return products.value.filter(p => p.is_in_stock === true)
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
    // Status
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