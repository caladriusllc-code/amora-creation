<template>
    <div class="main-layout">
        <Mainheader/>
        <product-grid
            title="Produits de la catégorie"
            subtitle="Découvrez tous les produits de la catégorie"
            :collection-id="1"
        />
        <FooterSection/>
    </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import Mainheader from '../../components/navigator/header.vue'
import productGrid from '~/components/layout/productGrid.vue';
import FooterSection from '~/components/layout/footerSection.vue';
export default {

    components:{
        Mainheader,
        productGrid,
        FooterSection
    },

    setup(){

        const route = useRoute();

        return{
            route,
        }
    }

}
</script>

<style>

</style>