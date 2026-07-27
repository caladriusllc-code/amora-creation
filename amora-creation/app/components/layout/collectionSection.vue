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
      <article v-for="collection in productStore.collections" :key="collection.id" class="collection-card">
        <div class="collection-image" :style="{ backgroundImage: `url(${placeholderImage(collection.slug)})` }" />
        <div class="collection-content">
          <h3>{{ collection.name }}</h3>
          <p>{{ collection.description || 'Collection saisonnière à découvrir.' }}</p>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useProductStore } from '../../stores/productStore'

const productStore = useProductStore()

onMounted(async () => {
  if (!productStore.collections.length) {
    await productStore.fetchCollections()
  }
})

const placeholderImage = (slug: string) => {
  const encoded = encodeURIComponent(slug || 'collection')
  return `https://images.unsplash.com/featured/?fashion,${encoded}&w=900&q=80`
}
</script>

<style scoped>
.collection-section {
  padding: 4rem 2rem;
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
  border-radius: 24px;
  overflow: hidden;
  background: white;
  box-shadow: 0 18px 35px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  min-height: 320px;
}

.collection-image {
  min-height: 220px;
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
</style>
