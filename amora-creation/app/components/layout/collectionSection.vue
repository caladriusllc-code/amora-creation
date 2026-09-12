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
/* =========================================
   CONTENEUR GLOBAL
   ========================================= */
.collection-section {
  padding: 8rem 1.5rem 4rem 1.5rem; /* Ajusté pour compenser la navbar et aérer le bas */
  background-color: #fafafa;
  text-align: center;
  min-height: 100vh;
}

.section-header {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  color: #6b7280;
  font-size: 1.125rem;
  max-width: 640px;
  margin: 0 auto;
}

.loading-state,
.error-state {
  color: #374151;
  font-size: 1rem;
  padding: 4rem 0;
}

/* =========================================
   GRILLE RESPONSIVE SANS MEDIA QUERY
   ========================================= */
.collections-grid {
  display: grid;
  /* La grille s'adapte automatiquement selon l'écran (mobile, tablette, desktop) */
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2.5rem 2rem;
  justify-items: center;
  max-width: 1280px; /* Aligné avec le reste de la boutique */
  margin: 0 auto;
}

/* =========================================
   CARTES DE COLLECTION
   ========================================= */
.collection-card {
  width: 100%;
  max-width: 350px; /* Donne un peu plus d'espace pour de belles images */
  height: 100%; /* S'assure que toutes les cartes ont la même hauteur visuelle[cite: 1, 3] */
  border-radius: 4px;
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
  flex-grow: 1; /* Pousse le contenu pour occuper l'espace restant */
}

.collection-content h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.collection-content p {
  color: #4b5563;
  line-height: 1.6;
  margin: 0;
}

.collection-button {
  margin-top: auto; /* Aligne toujours le bouton parfaitement en bas, quelle que soit la longueur du texte */
  align-self: flex-start;
  border: none;
  background: #111827;
  color: white;
  border-radius: 999px;
  padding: 0.7rem 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.collection-button:hover {
  background-color: #374151;
}
</style>