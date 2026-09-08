<template>
    <section class="main-layout">
        <div v-if="isLoading" class="pic-background skeleton-bg">
            <div class="overlay skeleton-overlay">
                <div class="skeleton skeleton-title"></div>
                <div class="skeleton skeleton-subtitle"></div>
                <div class="skeleton skeleton-btn"></div>
            </div>
        </div>

        <div v-else class="pic-background" :style="heroStyle">
            <div class="overlay">
                <h1>{{ title }}</h1>
                <p>{{ subtitle }}</p>
                <goToButton @click="scrollToGrid" label="Découvrez-nous"/>
            </div>
        </div>

        <div class="about-section flex items-center justify-center gap-4">

            <div class="about-title">
                
                <h2 class="text-xl align-start">description</h2>

                <p class="text-3xl max-w-2xl ">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. 
                    Nobis, <span>optio? Asperiores quibusdam nostrum qui magnam</span> ut 
                    facere optio tempora! Voluptas minima at illo unde maiores. 
                    Dignissimos praesentium quaerat officiis distinctio?
                </p>

            </div>


        </div>

        <div class="about-section flex items-center justify-center gap-4">
            <featuresCards />
            <featuresCards />
            <featuresCards />
        </div>

        
    </section>
</template>

<script>
import { computed, onMounted } from 'vue'
import goToButton from '../buttons/goToButton.vue'
import { useProductStore } from '../../stores/productStore'
import productGrid from './productGrid.vue'
import skeleton from '../tools/skeleton.vue'
import featuresCards from '../cards/featuresCards.vue'

export default {
    name: 'HeroSection',
    components: {
        goToButton,
        productGrid,
        skeleton,
        featuresCards
    },

    props: {
        title: {
            type: String,
            default: 'Amora Création'
        },
        subtitle: {
            type: String,
            default: 'Qui sommes-nous ?'
        }
    },

    setup(){
        const productStore = useProductStore()

        // 1. État de chargement des collections pour le Hero
        const isLoading = computed(() => {
            return productStore.collectionsLoading || productStore.collections.length === 0
        })

        const featuredCollection = computed(() => {
            if (!productStore.collections.length) return null
            return productStore.collections.find((collection) => collection.is_featured) || productStore.collections[0]
        })

        // 2. Gestion de l'image de fond uniquement si elle existe
        const backgroundImage = computed(() => {
            if (featuredCollection.value?.image) {
                return featuredCollection.value.image
            }
            return null
        })

        // 3. Style réactif pour l'arrière-plan
        const heroStyle = computed(() => {
            if (backgroundImage.value) {
                return { backgroundImage: `url(${backgroundImage.value})` }
            }
            return { backgroundColor: '#1a1a1a' }
        })

        const scrollToGrid = ()=> {
            const element = document.getElementById("grid-products")
            if(element){
                element.scrollIntoView({behavior: 'smooth'})
            }
        }

        onMounted(async () => {
            if (!productStore.collections.length) {
                await productStore.fetchCollections()
            }
        })

        return {
            productStore,
            isLoading,
            featuredCollection,
            heroStyle,
            scrollToGrid
        }
    },
}
</script>

<style scoped>
/* --- Section 1 : Le Hero --- */
.pic-background {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100vh;
    min-height: 400px;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    position: relative;
}

.collection-section {
    padding: 5rem 2rem; /* Espace en haut et en bas de la grille */
    width: 100%;
    display: flex;
    justify-content: center; /* Centre la grille et le skeleton */
}

.overlay {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.overlay h1 {
    font-size: 3rem;
    color: #fff;
    font-weight: 500;
    margin-bottom: 1rem;
    text-align: center;
}

.overlay p {
    font-size: 1.5rem;
    color: #fff;
    margin-bottom: 1rem;
    text-align: center;
}

/* =========================================
   💀 SKELETON STYLES (Animations de chargement)
   ========================================= */

@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

.skeleton {
    background: #e0e0e0;
    background-image: linear-gradient(90deg, #e0e0e0 0px, #af3232 40px, #e0e0e0 80px);
    background-size: 1000px 100%;
    animation: shimmer 2s infinite linear;
    border-radius: 4px;
}

.skeleton-bg {
    background: #d3d3d3;
}

.skeleton-overlay {
    background-color: rgba(0, 0, 0, 0.1);
}

.skeleton-title {
    width: 300px;
    height: 3.5rem;
    margin-bottom: 1rem;
    border-radius: 8px;
}

.skeleton-subtitle {
    width: 250px;
    height: 1.5rem;
    margin-bottom: 1.5rem;
}

.skeleton-btn {
    width: 180px;
    height: 50px;
    border-radius: 25px;
}

.collection-section {
    padding: 5rem 2rem;
    background-color: #fafafa;
    text-align: center;
}

.collection-section h2 {
    font-size: 2.5rem;
    color: #333;
    margin-bottom: 3rem;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2.5rem;
    max-width: 1200px;
    margin: 0 auto;
}

.about-title{
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.about-section{
    min-height:50vh;
    width: 100%;
    padding: 2rem;
    background-color: #ebebeb;
}

.about-section h2{
    background: #fff;
    padding: 0.5rem;
    width: fit-content;
    border-radius: 1.5rem;
}

.about-section p {
    width: 100%;
    line-height: 1.5;
    color: #767676;
    font-weight: 400;
}

.about-section p span{
    width: 100%;
    line-height: 1.5;
    color: #1f1f1f;
    font-weight: 600;
}

@media (max-width: 768px) {
    .pic-background {
        height: 80vh;
        min-height: 300px;
    }

    .skeleton-title {
        width: 80%;
        height: 2.5rem;
    }

    .skeleton-subtitle {
        width: 60%;
    }
}
</style>
