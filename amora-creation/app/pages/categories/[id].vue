<template>
    <div class="page-container">
        <Mainheader theme="dark" @toggle-cart="toggleCart"/>
        <categoryWithProducts />
        <FooterSection/>
        <cartModale :isOpen="isCartOpen" @close="toggleCart"/>
    </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import Mainheader from '../../components/navigator/header.vue'
import categoryWithProducts from '~/components/layout/categoryWithProducts.vue';
import FooterSection from '~/components/layout/footerSection.vue';
import cartModale from '~/components/modale/cartModale.vue'

export default {

    components:{
        Mainheader,
        FooterSection,
        categoryWithProducts,
        cartModale
    },

    setup(){

        const route = useRoute();
        const isCartOpen = ref<boolean>(false);

        function toggleCart() {
            isCartOpen.value = !isCartOpen.value;
        }

        return{
            route,
            isCartOpen,
            toggleCart
        }
    }

}
</script>

<style scoped>
.page-container {
  background-color: #ffffff;
  min-height: 100vh;
}
</style>
