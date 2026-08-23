<template>
  <div class="checkbox-wrapper" :class="{ 'has-error': errorMessage }">
    <label class="checkbox-label">
      <input
        type="checkbox"
        class="hidden-input"
        :checked="modelValue"
        @change="handleChange"
        v-bind="$attrs"
      />
      <!-- Fausse case à cocher pour un design 100% personnalisable -->
      <div class="custom-box">
        <svg v-if="modelValue" xmlns="http://www.w3.org/2000/svg" class="check-icon" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
      </div>

      <!-- Texte et lien -->
      <span class="label-text">
        J'ai lu et j'accepte les
        <a href="/cgv" target="_blank" class="cgv-link" @click.stop>conditions générales de vente</a>.
      </span>
    </label>

    <!-- Message d'erreur -->
    <div v-if="errorMessage" class="error-message">
      <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>{{ errorMessage }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean;
  errorMessage?: string;
}>();

const emit = defineEmits(['update:modelValue', 'change']);

const handleChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.checked);
  emit('change', target.checked); // Pratique pour effacer l'erreur au clic
};
</script>

<style scoped>
.checkbox-wrapper {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  gap: 12px;
}

.hidden-input {
  /* On cache l'input natif pour le remplacer par notre design */
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.custom-box {
  width: 20px;
  height: 20px;
  border: 2px solid #d1d5db;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin-top: 2px;
}

/* État coché */
.hidden-input:checked ~ .custom-box {
  background-color: #111827; /* Noir Amora */
  border-color: #111827;
}

.check-icon {
  width: 14px;
  height: 14px;
  color: white;
}

/* État d'erreur */
.has-error .custom-box {
  border-color: #ef4444; /* Rouge erreur */
  background-color: #fef2f2;
}

.label-text {
  font-size: 0.95rem;
  color: #374151;
  line-height: 1.4;
}

.cgv-link {
  color: #111827;
  text-decoration: underline;
  font-weight: 500;
}

.cgv-link:hover {
  color: #4b5563;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #ef4444;
  font-size: 0.85rem;
  margin-top: 4px;
}

.error-icon {
  width: 16px;
  height: 16px;
}
</style>
