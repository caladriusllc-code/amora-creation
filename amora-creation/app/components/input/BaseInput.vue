<template>
  <div 
    class="search-wrapper" 
    :class="{ 'is-focused': isFocused, 'has-error': errorMessage }"
  >
    <input
      :type="type"
      class="search-input"
      :value="modelValue"
      :placeholder="placeholder"
      @input="handleInput"
      @focus="isFocused = true"
      @blur="isFocused = false"
      v-bind="$attrs"
    />
    
    <div v-if="errorMessage" class="flex items-center mt-2 text-sm text-red-500">
      <svg 
        class="w-4 h-4 mr-1.5 fill-current" 
        xmlns="http://www.w3.org/2000/svg" 
        viewBox="0 0 20 20"
      >
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      <span>{{ errorMessage }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
  name: 'CustomInput',
  props: {
    modelValue: {
      type: [String, Number], // Accepte String ou Number (utile si type="number")
      default: ""
    },
    placeholder: {
      type: String,
      default: 'Rechercher...'
    },
    type: {
      type: String,
      default: 'text' // Par défaut c'est du texte, mais modifiable (email, password...)
    },
    errorMessage: {
      type: String,
      default: '' // Si vide, pas d'erreur affichée
    }
  },
  emits: ['update:modelValue', 'search', 'clear'],
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

    return {
      isFocused,
      handleInput,
      clearSearch
    }
  }
}
</script>

<style scoped>
.search-wrapper {
  position: relative;
  width: 100%;
}

.search-input {
  width: 100%;
  padding: 16px;
  font-size: 0.95rem;
  border-radius: 4px;
  color: #1f2937;
  transition: all 0.2s ease;
  border: 1px solid #d5d9df;
  outline: none; /* Supprime l'outline par défaut du navigateur */
}

/* État focus normal */
.is-focused .search-input {
  background-color: #ffffff;
  border-color: #3b82f6; /* Bleu par défaut */
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* État erreur (écrase la bordure normale) */
.has-error .search-input {
  border-color: #ef4444; /* Rouge Tailwind */
}

/* État focus ET erreur (Garde le focus en rouge) */
.has-error.is-focused .search-input {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}

.clear-button {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%); /* Centrage vertical parfait */
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: var(--icon-color, #9ca3af);
  display: flex;
  align-items: center;
  border-radius: 50%;
}

.clear-button:hover {
  background-color: #e5e7eb;
  color: #4b5563;
}

.clear-button svg {
  width: 16px;
  height: 16px;
}
</style>