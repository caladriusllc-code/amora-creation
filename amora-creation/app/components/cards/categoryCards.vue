<template>
    <div class="category-card" @click="$emit('click')">
        <div class="image-wrapper">
          <img :src="image" :alt="title" class="category-image" />
          <div class="overlay"></div>
        </div>
        
        <div class="card-footer w-full flex flex-row items-center justify-between mt-4">
            <div class="category-info">
                <h3 class="category-title">{{ title }}</h3>
                <p class="category-action">Découvrir la catégorie</p>
            </div>
            
            <div class="arrow-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
                </svg>
            </div>
        </div>
      </div>
</template>

<script>
export default {
    name: 'categoryCards',
    emits: ['click'],
    props: {
        image: {
            type: String,
            required: true
        },
        title: {
            type: String, // ex: "Robes & Combinaisons"
            required: true
        }
    }
}
</script>

<style scoped>
    .category-card {
        flex-shrink: 0;
        width: 220px;
        scroll-snap-align: start;
        cursor: pointer;
        /* Animation fluide sur toute la carte */
        transition: transform 0.3s ease; 
    }

    /* Le texte de la catégorie change de couleur quand on survole la carte */
    .category-card:hover .category-title {
        color: #6b7280; /* Un gris élégant au survol */
    }

    .category-card:hover .arrow-icon {
        transform: translateX(5px); /* La flèche avance un peu */
    }

    .image-wrapper {
        /* Format Portrait (3/4) : idéal pour la mode ! */
        aspect-ratio: 3 / 4; 
        position: relative;
        background-color: #f3f3f3;
        border-radius: 4px;
        overflow: hidden;
        margin-bottom: 12px;
    }

    .category-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.7s ease; /* Transition un peu plus lente pour le côté chic */
    }

    /* Zoom sur l'image au survol */
    .category-card:hover .category-image {
        transform: scale(1.05);
    }

    .category-info {
        font-family: 'Urbanist', sans-serif;
    }

    .category-title {
        font-weight: 800;
        color: #111827;
        margin: 0 0 4px 0;
        font-size: 16px;
        text-transform: uppercase;
        transition: color 0.3s ease;
    }

    .category-action {
        font-weight: 500;
        color: #6b7280;
        font-size: 13px;
        margin: 0;
    }

    .arrow-icon {
        width: 20px;
        height: 20px;
        color: #111827;
        transition: transform 0.3s ease;
    }
</style>