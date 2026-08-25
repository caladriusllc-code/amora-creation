<template>
    <div v-if="colors.length > 0" class="color-selector-container">
        <h3 class="color-title">
            Couleurs disponibles 
            <span v-if="selectedColor" class="selected-text">- {{ selectedColor.name }}</span>
        </h3>
        
        <div class="colors-row">
            <button 
                v-for="color in colors" 
                :key="color.id"
                class="color-circle-wrapper"
                :class="{ 'is-selected': selectedColor?.id === color.id }"
                @click="selectColor(color)"
                :aria-label="`Sélectionner la couleur ${color.name}`"
                :title="color.name"
            >
                <span 
                    class="color-circle" 
                    :style="{ backgroundColor: color.hex_code || '#cccccc' }"
                ></span>
            </button>
        </div>
    </div>
</template>

<script lang="ts">
import { ref, computed, defineComponent, PropType } from 'vue';

// On définit la structure d'une couleur (depuis le backend)
interface ColorType {
    id: number;
    name: string;
    hex_code: string | null; // Le code couleur HTML (ex: #000000)
}

export default defineComponent({
    name: 'ProductColors',
    props: {
        variants: {
            type: Array as PropType<any[]>,
            default: () => []
        }
    },
    emits: ['color-selected'], // Permet d'envoyer la couleur choisie au parent
    setup(props, { emit }) {
        // Extraire les couleurs uniques des variantes du backend
        const colors = computed(() => {
            if (!props.variants || props.variants.length === 0) return [];
            
            // Créer une Map pour garder les couleurs uniques par ID
            const uniqueColors = new Map();
            props.variants.forEach(variant => {
                if (variant.color && !uniqueColors.has(variant.color.id)) {
                    uniqueColors.set(variant.color.id, variant.color);
                }
            });
            
            return Array.from(uniqueColors.values());
        });

        // État pour stocker la couleur actuellement sélectionnée (par défaut, on peut présélectionner la 1ère)
        const selectedColor = computed(() => {
            return colors.value.length > 0 ? colors.value[0] : null;
        });

        // Fonction déclenchée au clic
        const selectColor = (color: ColorType) => {
            emit('color-selected', color); // Prévient le composant parent
        };

        return {
            colors,
            selectedColor,
            selectColor
        };
    }
});
</script>

<style scoped>
.color-selector-container {
    width: 100%;
    padding: 0.5rem;
}

.color-title {
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
    font-style: italic;
}

/* Conteneur de la ligne de couleurs */
.colors-row {
    display: flex;
    flex-direction: row;
    gap: 16px; /* Espace entre les couleurs */
    overflow-x: auto;
    padding: 4px; /* Un peu d'espace pour l'anneau de sélection */
    
    /* Cache la barre de défilement par défaut */
    scrollbar-width: none;
    -ms-overflow-style: none;
}
.colors-row::-webkit-scrollbar {
    display: none;
}

/* Le bouton qui entoure la couleur (invisible par défaut, sert pour l'anneau de sélection) */
.color-circle-wrapper {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background: transparent;
    border: 1px solid transparent; /* Pas de bordure par défaut */
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    padding: 0;
    transition: all 0.3s ease;
    flex-shrink: 0;
}

/* Le rond de couleur lui-même */
.color-circle {
    display: block;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 1px solid rgba(0, 0, 0, 0.1); /* Légère bordure pour les couleurs claires comme le blanc */
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1); /* Petit effet de profondeur */
}

/* Effet au survol */
.color-circle-wrapper:hover {
    transform: scale(1.1);
}

/* STYLE QUAND LA COULEUR EST SÉLECTIONNÉE */
.color-circle-wrapper.is-selected {
    border: 1px solid #333; /* Apparition de l'anneau chic autour de la couleur */
}
</style>