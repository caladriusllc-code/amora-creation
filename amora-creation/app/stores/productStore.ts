import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useNuxtApp } from '#app'

export interface Category {
  id?: number
  name: string
  slug: string
  description?: string
  image?: string
}

export interface CategoryWithProducts extends Category {
  products: Product[]
}

export interface Collection {
  id?: number
  name: string
  slug: string
  description?: string
  image?: string
}

export interface CollectionWithProducts extends Collection {
  products: Product[]
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

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export const useProductStore = defineStore('product', () => {
  const { $api } = useNuxtApp()

  const products = ref<Product[]>([])
  const currentProduct = ref<Product | null>(null)
  const categories = ref<Category[]>([])
  const collections = ref<Collection[]>([])

  const categoryWithProducts = ref<CategoryWithProducts | null>(null)
  const collectionWithProducts = ref<CollectionWithProducts | null>(null)

  const isLoading = ref<boolean>(false)
  const categoriesLoading = ref<boolean>(false)
  const collectionsLoading = ref<boolean>(false)
  const categoryProductsLoading = ref<boolean>(false)
  const collectionProductsLoading = ref<boolean>(false)

  const error = ref<string | null>(null)
  const categoriesError = ref<string | null>(null)
  const collectionsError = ref<string | null>(null)
  const categoryProductsError = ref<string | null>(null)
  const collectionProductsError = ref<string | null>(null)

  const fetchProducts = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await $api<PaginatedResponse<Product> | Product[]>('/product/products/')
      products.value = 'results' in response ? response.results : response
    } catch (err: any) {
      error.value = err?.data?.message || "Impossible de charger les produits d'Amora création."
      console.error('Erreur fetchProducts:', err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchProductBySlug = async (slug: string) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await $api<Product>(`/product/products/${slug}/`)
      currentProduct.value = response
    } catch (err: any) {
      error.value = err?.data?.message || 'Ce produit est introuvable.'
      console.error(`Erreur fetchProductBySlug (${slug}):`, err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchCategories = async () => {
    categoriesLoading.value = true
    categoriesError.value = null
    try {
      const response = await $api<PaginatedResponse<Category> | Category[]>('/product/categories/')
      categories.value = 'results' in response ? response.results : response
    } catch (err: any) {
      categoriesError.value = 'Impossible de charger les catégories.'
      console.error('Erreur fetchCategories:', err)
    } finally {
      categoriesLoading.value = false
    }
  }

  const fetchCollections = async () => {
    collectionsLoading.value = true
    collectionsError.value = null
    try {
      const response = await $api<PaginatedResponse<Collection> | Collection[]>('/product/collections/')
      collections.value = 'results' in response ? response.results : response
    } catch (err: any) {
      collectionsError.value = 'Impossible de charger les collections.'
      console.error('Erreur fetchCollections:', err)
    } finally {
      collectionsLoading.value = false
    }
  }

  const fetchCategoryWithProducts = async (id: string | number) => {
    categoryProductsLoading.value = true
    categoryProductsError.value = null
    categoryWithProducts.value = null

    try {
      const response = await $api<CategoryWithProducts>(`/product/categories/${id}/products/`, { method: 'GET' })
      categoryWithProducts.value = response
    } catch (err: any) {
      categoryProductsError.value = err?.data?.message || 'Impossible de charger cette catégorie et ses produits.'
      console.error(`Erreur fetchCategoryWithProducts (${id}):`, err)
    } finally {
      categoryProductsLoading.value = false
    }
  }

  const fetchCollectionWithProducts = async (identifier: string | number) => {
    collectionProductsLoading.value = true
    collectionProductsError.value = null
    collectionWithProducts.value = null

    try {
      if (!products.value.length) {
        await fetchProducts()
      }

      if (!collections.value.length) {
        await fetchCollections()
      }

      const currentCollection = collections.value.find((collection) => {
        return String(collection.id) === String(identifier) || collection.slug === String(identifier)
      })

      const matchedProducts = products.value.filter((product) => {
        if (!product.collection) return false

        if (typeof product.collection === 'object') {
          return String(product.collection.id) === String(identifier) || product.collection.slug === String(identifier)
        }

        return String(product.collection) === String(identifier) || String(product.collection) === String(currentCollection?.id)
      })

      if (currentCollection) {
        collectionWithProducts.value = {
          ...currentCollection,
          products: matchedProducts,
        }
        return
      }

      const fallbackCollection = products.value
        .find((product) => typeof product.collection === 'object' && product.collection?.slug === String(identifier))
        ?.collection as Collection | undefined

      if (fallbackCollection) {
        collectionWithProducts.value = {
          ...fallbackCollection,
          products: matchedProducts,
        }
        return
      }

      collectionWithProducts.value = {
        id: Number(identifier) || undefined,
        name: 'Collection',
        slug: String(identifier),
        description: 'Aucun produit n’a été trouvé pour cette collection.',
        products: [],
      }
    } catch (err: any) {
      collectionProductsError.value = err?.data?.message || 'Impossible de charger cette collection et ses produits.'
      console.error(`Erreur fetchCollectionWithProducts (${identifier}):`, err)
    } finally {
      collectionProductsLoading.value = false
    }
  }

  const inStockProducts = computed<Product[]>(() => {
    return products.value.filter((p) => p.is_in_stock === true)
  })

  const fetchProductsByCategories = fetchCategoryWithProducts

  return {
    products,
    currentProduct,
    categories,
    collections,
    categoryWithProducts,
    collectionWithProducts,
    isLoading,
    error,
    categoriesLoading,
    categoriesError,
    collectionsLoading,
    collectionsError,
    categoryProductsLoading,
    categoryProductsError,
    collectionProductsLoading,
    collectionProductsError,
    fetchProducts,
    fetchProductBySlug,
    fetchCategories,
    fetchCollections,
    fetchCategoryWithProducts,
    fetchCollectionWithProducts,
    fetchProductsByCategories,
    inStockProducts,
  }
})
