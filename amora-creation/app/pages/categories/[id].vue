<template>
    <div class="page-container">
        <Mainheader theme="black"/>
        <categoryWithProducts />
        <FooterSection/>
    </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import Mainheader from '../../components/navigator/header.vue'
import categoryWithProducts from '~/components/layout/categoryWithProducts.vue';
import FooterSection from '~/components/layout/footerSection.vue';
export default {

    components:{
        Mainheader,
        FooterSection,
        categoryWithProducts
    },

    setup(){

        const route = useRoute();

        return{
            route,
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