<template>
    <button class="shop-button">
        <span>{{ label }}</span>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z" />
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
  min-width: 200px;
  height: 50px;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  border: none;
  background-color: #000;
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  gap: 1rem;
  transition: ease-in-out 0.5s;
}

.shop-button:hover {
    transition: ease-in-out 0.3s;
    transform: translateY(-3px);
}

</style>