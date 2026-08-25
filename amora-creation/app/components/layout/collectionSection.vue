<template>
  <section class="collection-section">
    <div class="section-header">
      <h2 class="section-title">Nos Collections</h2>
      <p class="section-subtitle">Découvrez les collections actives directement depuis le backend.</p>
    </div>

    <div v-if="productStore.collectionsLoading" class="loading-state">
      <p>Chargement des collections...</p>
    </div>

    <div v-else-if="productStore.collectionsError" class="error-state">
      <p>{{ productStore.collectionsError }}</p>
    </div>

    <div v-else class="collections-grid">
      <article
        v-for="collection in productStore.collections"
        :key="collection.id"
        class="collection-card"
        @click="goToCollection(collection.slug)"
      >
        <div class="collection-image" :style="{ backgroundImage: `url(${getCollectionImage(collection)})` }" />
        <div class="collection-content">
          <h3>{{ collection.name }}</h3>
          <p>{{ collection.description || 'Collection saisonnière à découvrir.' }}</p>
          <button type="button" class="collection-button">Voir la collection</button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from '../../stores/productStore'

const productStore = useProductStore()
const router = useRouter()

onMounted(async () => {
  if (!productStore.collections.length) {
    await productStore.fetchCollections()
  }
})

const goToCollection = (slug: string) => {
  router.push(`/collection/${slug}`)
}

const placeholderImage = (slug: string) => {
  const encoded = encodeURIComponent(slug || 'collection')
  return `https://images.unsplash.com/featured/?fashion,${encoded}&w=900&q=80`
}

const getCollectionImage = (collection: any) => {
  if (collection.image) {
    return collection.image
  }

  return placeholderImage(collection.slug)
}
</script>

<style scoped>
.collection-section {
    padding: 8rem 1rem 1rem 1rem;
    background-color: #fafafa;
    text-align: center;
}

.section-header {
    margin-bottom: 2rem;
}

.section-title {
    font-size: 2.25rem;
    color: #111827;
    margin-bottom: 0.5rem;
}

.section-subtitle {
    color: #6b7280;
    max-width: 640px;
    margin: 0 auto;
}

.loading-state,
.error-state {
    color: #374151;
    font-size: 1rem;
    padding: 2rem 0;
}

.collections-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}

.collection-card {
    max-width: 320px;
    border-radius: 24px;
    overflow: hidden;
    background: white;
    box-shadow: 0 18px 35px rgba(15, 23, 42, 0.08);
    display: flex;
    flex-direction: column;
    min-height: 480px;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.collection-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 22px 40px rgba(15, 23, 42, 0.12);
}

.collection-image {
    min-height: 320px;
    background-size: cover;
    background-position: center;
}

.collection-content {
    padding: 1.5rem;
    text-align: left;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.collection-content h3 {
    font-size: 1.25rem;
    color: #111827;
    margin: 0;
}

.collection-content p {
    color: #4b5563;
    line-height: 1.6;
    margin: 0;
}

.collection-button {
    margin-top: 0.25rem;
    align-self: flex-start;
    border: none;
    background: #111827;
    color: white;
    border-radius: 999px;
    padding: 0.7rem 1.1rem;
    font-weight: 600;
    cursor: pointer;
}
</style>
