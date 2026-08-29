<template>
    <div class="search-container" :class="{ 'is-focused': isFocused, 'has-value': !!modelValue }">
        <div class="search-wrapper">
          <span class="search-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
            </svg>
          </span>

          <input
            type="text"
            class="search-input"
            :value="modelValue"
            :placeholder="placeholder"
            @input="handleInput"
            @focus="isFocused = true"
            @blur="handleBlur"
            v-bind="$attrs"
          />

          <button
            v-if="modelValue"
            type="button"
            class="clear-button"
            @click="clearSearch"
            aria-label="Effacer la recherche"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
            </svg>
          </button>

          <!-- ⚡️ Boîte de résultats calquée sur le design du panier -->
          <Transition name="fade">
            <div
              v-if="isFocused && modelValue"
              class="result-box"
              @mousedown.prevent
            >
              <div v-if="isLoading" class="result-message">
                Recherche en cours...
              </div>

              <div v-else-if="results.length === 0" class="result-message">
                Aucune image trouvée pour "{{ modelValue }}"
              </div>

              <div v-else class="search-items-list">
                <div
                  v-for="(image, index) in results"
                  :key="index"
                  class="search-item"
                  @click="selectImage(image)"
                >
                  <div class="item-image-wrapper">
                    <img :src="image.images?.[0]?.image || image.image || '/placeholder.png'" :alt="image.name || 'Résultat de recherche'" class="item-image" />
                  </div>

                  <div class="item-details">
                    <h5 class="item-name">{{ image.name || 'Produit' }}</h5>
                    <p class="item-subtitle">Voir l'article</p>
                  </div>

                  <div class="item-actions">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="action-icon">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </Transition>
        </div>
    </div>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
    props: {
      placeholder: {
        type: String,
        default: 'Rechercher...'
      },
      modelValue: {
        type: String,
        default: ""
      },
      results: {
        type: Array,
        default: () => []
      },
      isLoading: {
        type: Boolean,
        default: false
      }
    },
    emits: ['update:modelValue', 'search', 'clear', 'select'],
    setup(props, { emit }) {
        const isFocused = ref(false);

        const handleInput = (event: Event) => {
            const value = (event.target as HTMLInputElement).value;
            emit('update:modelValue', value);
            emit('search', value);
        };

        const clearSearch = () => {
            emit('update:modelValue', '');
            emit('clear');
        };

        const handleBlur = () => {
            isFocused.value = false;
        };

        const selectImage = (image: any) => {
            emit('select', image);
            isFocused.value = false;
        };

        return {
            isFocused,
            handleInput,
            clearSearch,
            handleBlur,
            selectImage
        }
    }
}
</script>

<style scoped>
.search-container {
  --search-bg: white;
  --search-border: #e5e7eb;
  --search-focus: var(--primary-color, #111827);
  --icon-color: #9ca3af;
  width: 100%;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  transition: all 0.2s ease;
}

.search-icon {
  position: absolute;
  left: 12px;
  width: 20px;
  height: 20px;
  color: var(--icon-color);
  pointer-events: none;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 10px 40px 10px 42px;
  font-size: 0.95rem;
  background-color: var(--search-bg);
  border-radius: 8px;
  border: 1px solid var(--search-border);
  color: #1f2937;
  outline: none;
  transition: all 0.2s ease;
}

.is-focused .search-input {
  background-color: #ffffff;
  border-color: var(--search-focus);
  box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.1);
}

.is-focused .search-icon {
  color: var(--search-focus);
}

.clear-button {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: var(--icon-color);
  display: flex;
  align-items: center;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.clear-button:hover {
  background-color: #f3f4f6;
  color: #4b5563;
}

.clear-button svg {
  width: 16px;
  height: 16px;
}

/* =========================================
   BOÎTE DE RÉSULTATS (RESULT BOX)
   ========================================= */
.result-box {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 100%;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  padding: 16px;
  z-index: 50;
  max-height: 400px; /* Légèrement augmenté pour les grandes images */
  overflow-y: auto;
}

.result-message {
  text-align: center;
  color: #6b7280;
  font-size: 0.95rem;
  padding: 1rem 0;
}

/* =========================================
   LISTE DES RÉSULTATS (STYLE PANIER)
   ========================================= */
.search-items-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.search-item {
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem;
  border-bottom: 1px solid #f9f9f9;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.search-item:last-child {
  border-bottom: none;
}

.search-item:hover {
  background-color: #f9fafb;
}

/* Image du produit */
.item-image-wrapper {
  width: 60px; /* Adapté pour la barre de recherche */
  height: 75px;
  flex-shrink: 0;
  background: #f3f4f6;
  border-radius: 6px;
  overflow: hidden;
}

.item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Détails du produit */
.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.item-name {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-subtitle {
  margin: 0;
  font-size: 0.8rem;
  color: #6b7280;
}

/* Actions (Flèche) */
.item-actions {
  display: flex;
  align-items: center;
}

.action-icon {
  width: 18px;
  height: 18px;
  color: #9ca3af;
  transition: color 0.2s ease, transform 0.2s ease;
}

.search-item:hover .action-icon {
  color: #111827;
  transform: translateX(3px); /* Petit effet de glissement au survol */
}

/* Animation douce d'apparition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
