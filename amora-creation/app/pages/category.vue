<template>
    <div class="page-container">
        <Mainheader/>
        <main>
            <heroSection
                title="Robes de soirées"
                subtitle="Toutes nos robes de soirées"
                backgroundImage="https://images.unsplash.com/photo-1612336307429-8a898d10e223?q=80&w=987&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            />
            <productsCategory title="Catégories de produits"/>
            <productGrid 
            title="Nos produits les plus demandés"
            subtitle="Découvrez nos produits les plus demandés"
            :products="products"
            />

        </main>
        <footerSection/>
    </div>
</template>

<script lang="ts">
import Mainheader from '../components/navigator/header.vue'
import heroSection from '../components/layout/heroSection.vue';
import productsCategory from '../components/layout/ProductsCategory.vue'
import productGrid from '../components/layout/productGrid.vue';
import footerSection from '~/components/layout/footerSection.vue';

export default {
  components: {
    Mainheader,
    heroSection,
    productsCategory,
    productGrid,
    footerSection
  },
  setup() {
    const products = [
      {
        id:1,
        name:"Robe d'été Élégance",
        price:12000,
        image: 'https://images.unsplash.com/photo-1622122201714-77da0ca8e5d2?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fHJvYmVzfGVufDB8fDB8fHww', 
        sale:false,
      },
      {
        id:2,
        name:"Robe d'été Élégance",
        price:12000,
        image:"https://images.unsplash.com/photo-1596783047904-4000addd05cd?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MjB8fHJvYmVzfGVufDB8fDB8fHww",
        sale:false,
      },
      {
        id:3,
        name:"Robe d'été Élégance",
        price:12000,
        image:"https://plus.unsplash.com/premium_photo-1673758901405-32f0a6f625d4?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8cGFudGFsb24lMjBmZW1tZXN8ZW58MHx8MHx8fDA%3D",
        sale:false,
      },
      {
        id:4,
        name:"Ensemble stylé",
        price:12000,
        image:"https://images.unsplash.com/photo-1580651214613-f4692d6d138f?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8cGFudGFsb24lMjBmZW1tZXN8ZW58MHx8MHx8fDA%3D",
        sale:false,
      }
    ]

    const salesProducts = [
      {
        id:1,
        name:"Robe d'été Élégance",
        price:12000,
        image: 'https://images.unsplash.com/photo-1622122201714-77da0ca8e5d2?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTl8fHJvYmVzfGVufDB8fDB8fHww', 
        sale:true,
      },
      {
        id:2,
        name:"Robe d'été Élégance",
        price:12000,
        image:"https://images.unsplash.com/photo-1672783266337-e6d9b1e2c8d0?w=600&q=80",
        sale:true,
      },
      {
        id:3,
        name:"Robe d'été Élégance",
        price:12000,
        image:"https://images.unsplash.com/photo-1672783266337-e6d9b1e2c8d0?w=600&q=80",
        sale:true,
      },
      {
        id:4,
        name:"Ensemble stylé",
        price:12000,
        image:"https://images.unsplash.com/photo-1580651214613-f4692d6d138f?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8cGFudGFsb24lMjBmZW1tZXN8ZW58MHx8MHx8fDA%3D",
        sale:true,
      }
    ]
    return {
      products,
      salesProducts
    };
  }
}
</script>

<style scoped>
.page-container {
  background-color: #ffffff;
  min-height: 100vh;
}
</style>