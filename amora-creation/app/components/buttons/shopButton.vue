<template>
  <button class="shop-button">
    <span>Acheter maintenant</span>
  </button>
</template>

<script>
export default {
    name:'shopButton'

}
</script>

<style scoped>
.shop-button {
    width: 200px;
    padding: 0.7rem 1rem;
    border-radius: 4px;
    border: none;
    background-color: #fff;
    color: #000;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1rem;
    font-weight: 600;
}

</style>