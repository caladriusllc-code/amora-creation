<template>
    <div class="size-selector-container">
        <h3 class="size-title">Tailles disponibles <span v-if="selectedSize" class="selected-text">- Taille choisie : EU {{ selectedSize.eu }}</span></h3>
        
        <div class="sizes-row">
            <button 
                v-for="size in sizes" 
                :key="size.id"
                class="size-square"
                :class="{ 'is-selected': selectedSize?.id === size.id }"
                @click="selectSize(size)"
                aria-label="Sélectionner la taille"
            >
                <span class="size-label">EU {{ size.eu }}</span>
                <hr class="size-divider" />
                <span class="size-label">AF {{ size.af }}</span>
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { ref, defineComponent } from 'vue';

// On définit la structure d'une taille
interface SizeType {
    id: number;
    eu: number;
    af: number;
}

export default defineComponent({
    name: 'ProductSizes',
    emits: ['size-selected'], // Permet d'envoyer la taille sélectionnée au composant parent
    setup(props, { emit }) {
        // Liste de tes tailles (tu pourras plus tard les recevoir depuis une base de données)
        const sizes = ref<SizeType[]>([
            { id: 1, eu: 36, af: 38 },
            { id: 2, eu: 38, af: 40 },
            { id: 3, eu: 40, af: 42 },
            { id: 4, eu: 42, af: 44 },
            { id: 5, eu: 44, af: 46 },
            { id: 6, eu: 46, af: 48 },
        ]);

        // État pour stocker la taille actuellement cliquée
        const selectedSize = ref<SizeType | null>(null);

        // Fonction déclenchée au clic
        const selectSize = (size: SizeType) => {
            selectedSize.value = size;
            emit('size-selected', size); // Prévient le composant parent (ex: pour l'ajout au panier)
        };

        return {
            sizes,
            selectedSize,
            selectSize
        };
    }
});
</script>

<style scoped>
.size-selector-container {
    width: 100%;
    padding: 0.5rem;
}

.size-title {
    font-size: 1rem;
    font-weight: 600;
    color: #333;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.selected-text {
    font-weight: 400;
    color: #666;
    text-transform: none;
}

/* Conteneur de la ligne (scrollable sur petit écran si trop de tailles) */
.sizes-row {
    display: flex;
    flex-direction: row;
    gap: 12px;
    overflow-x: auto;
    padding-bottom: 8px; /* Pour laisser de la place au hover */
    
    /* Cache la barre de défilement par défaut */
    scrollbar-width: none;
    -ms-overflow-style: none;
}
.sizes-row::-webkit-scrollbar {
    display: none;
}

/* Le design des carrés */
.size-square {
    flex-shrink: 0;
    width: 70px;
    height: 70px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: transparent;
    border: 1px solid #ccc;
    border-radius: 4px; /* Coins légèrement arrondis */
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 0;
}

/* Texte à l'intérieur */
.size-label {
    font-size: 0.85rem;
    font-weight: 500;
    color: #555;
    transition: color 0.3s ease;
}

/* La petite ligne de séparation au milieu */
.size-divider {
    width: 40%;
    height: 1px;
    background-color: #ccc;
    border: none;
    margin: 6px 0;
    transition: background-color 0.3s ease;
}

/* Effet au survol de la souris (Desktop) */
.size-square:hover {
    border-color: #333;
}

/* STYLE QUAND LA TAILLE EST SÉLECTIONNÉE */
.size-square.is-selected {
    background-color: #333; /* Fond sombre chic */
    border-color: #333;
    transform: translateY(-2px); /* Petit effet de soulèvement */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.size-square.is-selected .size-label {
    color: #fff; /* Le texte devient blanc */
}

.size-square.is-selected .size-divider {
    background-color: #fff; /* La ligne devient blanche */
}
</style>