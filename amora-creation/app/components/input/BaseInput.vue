<template>
    <div class="search-wrapper">

        <input
            type="text"
            class="search-input"
            :value="modelValue"
            :placeholder="placeholder"
            @input="handleInput"
            @focus="isFocused = true"
            @blur="isFocused = false"
            v-bind="$attrs"
        />

    </div>
</template>

<script lang="ts">
import { ref } from 'vue';

interface Props {
  modelValue: string | number;
  placeholder?: string;
}
export default{
    props:{
      placeholder:{
        type:String,
        default:'Rechercher...'
      },
      modelValue:{
        type:String,
        default:""
      }
    },
    emits:['update:modelValue', 'search', 'clear'],
    setup(props, {emit}){
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

        return{
            isFocused,
            handleInput,
            clearSearch
        }
    }
}

</script>

<style scoped>

.search-wrapper{

}

.search-input {
  width: 100%;
  padding: 16px;
  font-size: 0.95rem;
  border-radius: 4px;
  color: #1f2937;
  outline: none;
  transition: all 0.2s ease;
  border: 1px solid #d5d9df;
}

.is-focused .search-input {
  background-color: #ffffff;
  border-color: var(--search-focus);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
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