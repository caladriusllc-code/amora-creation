<template>
  <div class="category-list">
    <button
      v-for="category in categories"
      :key="category.id"
      :class="{ active: activeCategory === category.id }"
      @click="setActive(category.id)"
    >
      {{ category.name }}
    </button>
  </div>
</template>

<script setup lang="ts">
// Plus besoin de 'ref', on utilise defineProps et defineEmits
import { defineProps, defineEmits } from 'vue'

// 1. Définition du type pour nos catégories
interface Category {
  id: string
  name: string
}

// 2. Déclaration des props reçues du parent
defineProps<{
  categories: Category[]
  activeCategory: string // L'ID de la catégorie actuellement sélectionnée
}>()

// 3. Déclaration de l'événement envoyé au parent
const emit = defineEmits<{
  (e: 'update:activeCategory', categoryId: string): void
}>()

// 4. Fonction déclenchée au clic
const setActive = (categoryId: string) => {
  // On prévient le parent qu'une nouvelle catégorie a été choisie
  emit('update:activeCategory', categoryId)
}
</script>

<style scoped>
.category-list {
  margin-top: 1.5rem;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem; /* Espacement entre les boutons */
  flex-wrap: wrap; /* Permet le retour à la ligne sur petit écran */
}

/* Style de base (inactif) */
.category-list button {
  background: #e0e0e0; /* Couleur neutre par défaut */
  border: none;
  padding: 0.75rem 1.25rem;
  cursor: pointer;
  color: #333;
  border-radius: 8px; /* Optionnel : bords arrondis */
  transition: all 0.2s ease-in-out;
}

.category-list button:hover {
  background: #d0d0d0;
}

/* Style de la catégorie active */
.category-list button.active {
  background: var(--primary-color, #007bff); /* Utilise ta variable, avec un bleu en secours */
  color: #fff;
}
</style>
