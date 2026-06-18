<template>
  <button class="cart-button">
    <svg 
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" viewBox="0 0 24 24" 
        stroke-width="1.5" 
        stroke="currentColor" class="size-6"
        v-if="!isLoading"
    >
        <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z" />
    </svg>
    <span class="loading loading-spinner loading-md" v-else></span>
  </button>
</template>

<script>
export default {

    name: 'cartButton',
    props:{
        isLoading: {
            type:Boolean, 
            default:false
        },
        
    }

}
</script>

<style scoped>

.cart-button{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 4px;
    background-color: #000;
    color: #fff;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

</style>