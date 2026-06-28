<template>
    <section class="main-layout">
        <div class="pic-background" :style="{ backgroundImage: `url(${backgroundImage})` }">
            <div class="overlay">
                <h1>{{ title }}</h1>
                <p>{{ subtitle }}</p>
                <goToButton @click="scrollToGrid"/>
            </div>
        </div>

        <product-grid />
    </section>
</template>

<script>
import goToButton from '../buttons/goToButton.vue';
import productCards from '../cards/productCards.vue';
import scrollBar from '../tools/scrollBar.vue';
import productGrid from '../layout/productGrid.vue'

export default {
    name: 'HeroSection',
    props:{
        title:{
            type: String,
            default: "Nouvelle collection"
        },
        subtitle:{
            type: String,
            default: "Découvrez nos dernières créations"
        },
        // Ajout de la troisième prop pour l'image
        backgroundImage:{
            type: String,
            default: "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        },
    },
    components: {
        goToButton,
        scrollBar,
        productCards,
        productGrid
    },

    setup(){

        const products = [
            { 
                id: 1, 
                name: "Robe d'été Élégance", 
                price:120, 
                image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=600&q=80" 
            },
            { 
                id: 2, 
                name: "Veste en Lin Classique", 
                price:150, 
                image: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600&q=80" 
            },
            { 
                id: 3, 
                name: "Chemisier Soie Douce", 
                price:85, 
                image: "https://images.unsplash.com/photo-1551163943-3f6a855d1153?w=600&q=80" 
            },
            { 
                id: 4, 
                name: "Pantalon Taille Haute", 
                price:95, 
                image: "https://images.unsplash.com/photo-1584370848010-d7fe6bc767ec?w=600&q=80" 
            }
        ]

        const scrollToGrid = ()=> {
            const element = document.getElementById("grid-products");

            if(element){
                element.scrollIntoView({behavior: 'smooth'})
            }
        }

        return{
            products,
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