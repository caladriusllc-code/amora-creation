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

        <div class="about-section flex flex-col items-center justify-center gap-8 py-16">
            
            <div class="about-title w-full max-w-4xl text-center flex flex-col items-center">
                <h2 class="text-xl">Notre Histoire</h2>
                <p class="text-3xl mt-4">
                    Amora Création est une maison dédiée à <span>l'élégance et la beauté féminine</span>. 
                    Nous concevons des pièces uniques qui subliment chaque silhouette, en alliant 
                    le raffinement des coupes à la noblesse des matières. Laissez-vous séduire par 
                    des créations pensées pour la femme moderne, audacieuse et distinguée.
                </p>
            </div>

            <!-- ⚡️ Les cartes avec les features intéressantes pour une boutique de dame -->
            <div class="flex flex-wrap items-center justify-center gap-6 mt-8">
                
                <featuresCards 
                    title="Qualité Supérieure" 
                    description="Des tissus soigneusement sélectionnés pour vous offrir un tombé parfait et une durabilité exceptionnelle au quotidien."
                >
                    <template #icon>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.61l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.536a.562.562 0 0 1-.84-.61l1.285-5.386a.562.562 0 0 0-.182-.557l-4.204-3.602a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
                        </svg>
                    </template>
                </featuresCards>

                <featuresCards 
                    title="Sur-Mesure & Confort" 
                    description="Chaque vêtement est pensé pour épouser vos formes et garantir une aisance absolue, tout en affirmant votre style."
                >
                    <template #icon>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M14.25 9.75 16.5 12l-2.25 2.25m-4.5 0L7.5 12l2.25-2.25M6 20.25h12A2.25 2.25 0 0 0 20.25 18V6A2.25 2.25 0 0 0 18 3.75H6A2.25 2.25 0 0 0 3.75 6v12A2.25 2.25 0 0 0 6 20.25Z" />
                        </svg>
                    </template>
                </featuresCards>

                <featuresCards 
                    title="Design Exclusif" 
                    description="Affirmez votre personnalité grâce à des designs originaux, des coupes modernes et des détails raffinés qui font la différence."
                >
                    <template #icon>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09l2.846.813-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                        </svg>
                    </template>
                </featuresCards>
                
            </div>
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
            default: 'Révélez votre élégance'
        }
    },

    setup(){
        const productStore = useProductStore()

        const isLoading = computed(() => {
            return productStore.collectionsLoading || productStore.collections.length === 0
        })

        const featuredCollection = computed(() => {
            if (!productStore.collections.length) return null
            return productStore.collections.find((collection) => collection.is_featured) || productStore.collections[0]
        })

        const backgroundImage = computed(() => {
            if (featuredCollection.value?.image) {
                return featuredCollection.value.image
            }
            return null
        })

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
   💀 SKELETON STYLES
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

/* =========================================
   SECTION À PROPOS
   ========================================= */
.about-title{
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.about-section{
    min-height: 50vh;
    width: 100%;
    padding: 4rem 2rem;
    background-color: #ebebeb;
}

.about-section h2{
    background: #1f1f1f;
    color: #fff;
    padding: 0.5rem 1.5rem;
    width: fit-content;
    border-radius: 1.5rem;
    text-transform: uppercase;
    font-weight: 600;
    font-size: 1.1rem;
    letter-spacing: 1px;
}

.about-section p {
    width: 100%;
    line-height: 1.6;
    color: #555555;
    font-weight: 400;
}

.about-section p span{
    width: 100%;
    line-height: 1.6;
    color: #1f1f1f;
    font-weight: 700;
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