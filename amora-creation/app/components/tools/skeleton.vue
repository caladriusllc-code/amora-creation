<template>
    <div class="skeleton-container">
        <div 
            v-for="n in 3" 
            :key="n" 
            class="skeleton-card category-card"
        >
            <div class="skeleton skeleton-image"></div>
            
            <div class="card-footer w-full flex flex-row items-center justify-between mt-4">
                <div class="category-info w-full">
                    <div class="skeleton skeleton-title"></div>
                    <div class="skeleton skeleton-action"></div>
                </div>
                
                <div class="skeleton skeleton-icon"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CategorySkeleton'
}
</script>

<style scoped>
/* =========================================
   🔧 DISPOSITION RESPONSIVE (3 sur PC, 1 sur Mobile)
   ========================================= */
.skeleton-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px; /* L'espacement entre tes cartes */
    width: 100%;
    overflow: hidden; /* Empêche le débordement horizontal pendant le chargement */
}

/* Base de la carte (identique à ton vrai composant) */
.category-card {
    flex-shrink: 0;
    width: 220px;
    cursor: default; /* Pas de pointeur pendant le chargement */
}

/* 📱 Sur Tablette et Mobile (moins de 992px) : on cache les cartes 2 et 3 */
@media (max-width: 991px) {
    .skeleton-card:nth-child(n+2) {
        display: none;
    }
}

/* =========================================
   💀 ANIMATIONS ET FORMES SKELETON
   ========================================= */
@keyframes shimmer {
    0% { background-position: -1000px 0; }
    100% { background-position: 1000px 0; }
}

/* Classe de base commune */
.skeleton {
    background: #e0e0e0;
    background-image: linear-gradient(90deg, #e0e0e0 0px, #f0f0f0 40px, #e0e0e0 80px);
    background-size: 1000px 100%;
    animation: shimmer 2s infinite linear;
    border-radius: 4px;
}

/* Remplacement de l'image wrapper */
.skeleton-image {
    aspect-ratio: 3 / 4;
    width: 100%;
    margin-bottom: 12px;
}

.category-info {
    display: flex;
    flex-direction: column;
    gap: 8px; /* Espace entre le titre et l'action */
    width: 100%;
}

/* Remplacement du h3 (Titre) */
.skeleton-title {
    height: 16px;
    width: 75%; /* Ne prend pas toute la largeur pour faire réaliste */
}

/* Remplacement du p (Action) */
.skeleton-action {
    height: 12px;
    width: 50%;
}

/* Remplacement du SVG (Flèche) */
.skeleton-icon {
    width: 24px;
    height: 24px;
    border-radius: 50%; /* On en fait un rond pour faire joli */
    flex-shrink: 0;
}
</style>