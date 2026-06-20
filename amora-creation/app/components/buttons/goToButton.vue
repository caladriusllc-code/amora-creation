<template>
  <button class="shop-button">
    <span>{{ label }}</span>
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
      <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3" />
    </svg>
  </button>
</template>

<script lang="ts">
export default {
  name:'shopButton',
  props:{
    label:{
      type:String,
      default: "Voir collection"
    }
  }

}
</script>

<style scoped>
.shop-button {
  max-width: 250px;
  padding: 0.7rem 1rem;
  border-radius: 4px;
  border: none;
  background-color: #fff;
  color: #000;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  gap: 1rem;
}

</style>