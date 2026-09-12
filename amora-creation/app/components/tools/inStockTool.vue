<template>
  <div class="instock-container">
    <div class="w-full flex gap-4" v-if="isInStock">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
        </svg>
        <p>En stock</p>
    </div>
    <div class="w-full flex gap-4" v-else>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12H9m12 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
        </svg>
        <p>Stock épuisé</p>
    </div>
  </div>
</template>

<script>
export default {

    props: {
        isInStock: {
            type: Boolean,
            default: true 
        }
    }

}
</script>

<style scoped>

.instock-container {
    width: 100%;
    display: flex;
    justify-content: start;
    gap: 1rem;
    border-radius: 8px;
    margin-top: 1rem;
}

</style>