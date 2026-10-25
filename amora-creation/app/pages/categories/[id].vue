<template>
    <div class="page-container">
        <Head>
            <title>Amora - Catégorie {{ title }}</title>
            <meta name="description" content="Gotics Business & Web Analytics Dashboard" />
        </Head>
        <Mainheader theme="black" @toggle-cart="toggleCart"/>
        <categoryWithProducts />
        <FooterSection/>
        <cartModale :isOpen="isCartOpen" @close="toggleCart"/>
    </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
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

        const title = computed(()=>{
            const slug = route.params.id
            return slug;
        })

        const isCartOpen = ref<boolean>(false);

        function toggleCart() {
            isCartOpen.value = !isCartOpen.value;
        }

        return{
            route,
            title,
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
