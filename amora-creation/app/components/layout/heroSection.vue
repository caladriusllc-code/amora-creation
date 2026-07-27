<template>
    <section class="main-layout">
        <div class="pic-background" :style="{ backgroundImage: `url(${backgroundImage})` }">
            <div class="overlay">
                <h1>{{ title }}</h1>
                <p>{{ subtitle }}</p>
                <goToButton @click="scrollToGrid"/>
            </div>
        </div>

        <productGrid
            v-if="featuredCollection" 
            :collection-id="featuredCollection.id" 
        />
    </section>
</template>

<script>
import { computed, onMounted } from 'vue'
import goToButton from '../buttons/goToButton.vue'
import { useProductStore } from '../../stores/productStore'
import productGrid from './productGrid.vue';

export default {
    name: 'HeroSection',
    components: {
        goToButton,
        productGrid
    },

    setup(){
        const productStore = useProductStore()

        const featuredCollection = computed(() => {
            return productStore.collections.find((collection) => collection.is_featured) || productStore.collections[0] || null
        })

        const title = computed(() => {
            return featuredCollection.value?.name || 'Nouvelle collection'
        })

        const subtitle = computed(() => {
            return featuredCollection.value?.description || 'Découvrez nos dernières créations'
        })

        const backgroundImage = computed(() => {
            // ✨ 1. Si on a uploadé une image dans Django, on l'utilise !
            if (featuredCollection.value?.image) {
                // Selon ta configuration Django, l'URL peut être relative. 
                // Si l'image ne s'affiche pas, dé-commente la ligne du dessous à la place :
                // return `http://127.0.0.1:8000${featuredCollection.value.image}`
                return featuredCollection.value.image
            }

            // ✨ 2. Plan B : Si la collection n'a pas d'image, on utilise Unsplash avec le slug
            if (featuredCollection.value?.slug) {
                return `https://images.unsplash.com/featured/?fashion,${encodeURIComponent(featuredCollection.value.slug)}&w=1170&q=80`
            }
            
            // ✨ 3. Plan C : Image par défaut ultime
            return 'https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
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

        return{
            featuredCollection, // ✨ AJOUT ICI : Il faut l'exporter pour l'utiliser dans le template
            title,
            subtitle,
            backgroundImage,
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
    
    /* Largeur totale */
    width: 100%;
    
    /* Hauteur pour ordinateur : 70% de l'écran, avec un minimum pour que le texte rentre */
    height: 70vh; 
    min-height: 400px; 
    
    /* L'image de fond a été retirée d'ici car elle est maintenant gérée dans le template ! */
    background-size: cover; /* L'image couvre tout l'espace sans se déformer */
    background-position: center; /* L'image reste bien centrée */
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
    font-weight: bold;
    margin-bottom: 1rem;
    text-align: center;
}

.overlay p {
    font-size: 1.5rem;
    color: #fff;
    margin-bottom: 1rem;
}

/* --- Section 2 : La galerie de la collection --- */
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

/* Grille responsive pour les vêtements */
.products-grid {
    display: grid;
    /* Crée automatiquement autant de colonnes de 280px minimum que possible */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2.5rem;
    max-width: 1200px;
    margin: 0 auto;
}

@media (max-width: 768px) {
    .pic-background {
        /* On réduit un peu la hauteur sur mobile pour que le contenu en dessous soit visible plus vite */
        height: 80vh;
        min-height: 300px; 
    }
}
</style>