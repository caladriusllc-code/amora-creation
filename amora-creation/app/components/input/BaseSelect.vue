<template>
  <div 
    class="select-wrapper" 
    :class="{ 'is-focused': isFocused, 'has-error': errorMessage }"
  >
    <select
      class="select-input"
      :value="modelValue"
      @change="handleChange"
      @focus="isFocused = true"
      @blur="isFocused = false"
      v-bind="$attrs"
    >
      <option v-if="placeholder" value="" disabled>
        {{ placeholder }}
      </option>
      
      <option 
        v-for="(option, index) in options" 
        :key="index" 
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>
    
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
import { ref, PropType } from 'vue';

// Définition de l'interface pour tes options
export interface SelectOption {
  label: string;
  value: string | number;
}

export default {
  name: 'BaseSelect',
  props: {
    modelValue: {
      type: [String, Number],
      default: ""
    },
    options: {
      type: Array as PropType<SelectOption[]>,
      required: true,
      default: () => []
    },
    placeholder: {
      type: String,
      default: 'Sélectionnez une option...'
    },
    errorMessage: {
      type: String,
      default: '' // Si vide, pas d'erreur affichée
    }
  },
  emits: ['update:modelValue', 'change'],
  setup(props, { emit }) {
    const isFocused = ref(false);

    const handleChange = (event: Event) => {
      const value = (event.target as HTMLSelectElement).value;
      emit('update:modelValue', value);
      emit('change', value);
    };

    return {
      isFocused,
      handleChange
    }
  }
}
</script>

<style scoped>
.select-wrapper {
  position: relative;
  width: 100%;
}

.select-input {
  width: 100%;
  padding: 16px;
  font-size: 0.95rem;
  border-radius: 4px;
  color: #1f2937;
  transition: all 0.2s ease;
  border: 1px solid #d5d9df;
  outline: none;
  background-color: #ffffff;
  cursor: pointer;
  
  /* Masque la flèche par défaut du navigateur pour la remplacer par une icône SVG personnalisée */
  appearance: none; 
  -webkit-appearance: none;
  -moz-appearance: none;
  
  /* Flèche SVG intégrée proprement en background */
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%239ca3af%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 16px top 50%;
  background-size: 12px auto;
}

/* Gère la couleur du texte si le placeholder est sélectionné */
.select-input:invalid {
  color: #9ca3af;
}

/* État focus normal */
.is-focused .select-input {
  background-color: #ffffff;
  border-color: #3b82f6; /* Bleu par défaut */
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

/* État erreur (écrase la bordure normale) */
.has-error .select-input {
  border-color: #ef4444; /* Rouge Tailwind */
}

/* État focus ET erreur (Garde le focus en rouge) */
.has-error.is-focused .select-input {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}
</style>