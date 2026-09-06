<template>
  <div class="pro-card">
    <div class="image-wrapper" @click="$emit('goToProductDetail')">
      <!-- ⚡️ Affiche le pourcentage s'il est fourni sous forme de texte, sinon affiche "Sale" par défaut -->
      <span v-if="sale" class="sale-badge">{{ typeof sale === 'string' ? sale : 'Sale' }}</span>
      
      <img
        :src="image"
        :alt="name"
        class="product-image"
        @error="handleImageError"
      />
    </div>
    
    <div class="card-footer w-full flex flex-row items-center justify-between">
      <div class="product-info">
        <h3 class="product-name">{{ name }}</h3>
        <div class="price flex items-center justify-between gap-4">
          <p class="product-price">{{ formatPrice(displayPrice) }}</p>
          <p v-if="hasDiscount" class="product-base-price">{{ formatPrice(basePrice) }}</p>
        </div>
      </div>
      <cart-button
        @click="$emit('addToCart')"
        :isLoading="isLoading"
      />
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import cartButton from '../buttons/cartButton.vue';
import { useCartStore } from '../../stores/cartStore';

export default {
  name: 'productCards',
  components: {
    cartButton,
  },
  props: {
    image: String,
    name: String,
    price: [Number, String], 
    basePrice: [Number, String],
    discountPrice: [Number, String],
    sale: [Boolean, String], // ⚡️ Accepte désormais le booléen classique OU la string "-20%"
    isLoading: Boolean,
  },
  emits: ['addToCart', 'goToProductDetail'],
  setup(props) {
    const cartStore = useCartStore();
    const displayPrice = computed(() => {
      return props.discountPrice !== null && props.discountPrice !== undefined
        ? props.discountPrice
        : props.price;
    });
    const hasDiscount = computed(() => {
      return props.discountPrice !== null && props.discountPrice !== undefined;
    });

    const formatPrice = (amount) => {
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        maximumFractionDigits: 0,
      }).format(amount || 0);
    };

    const handleImageError = (e) => {
      console.error('Erreur chargement image:', props.image, e);
      e.target.src =
        'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80';
    };

    return {
      cartStore,
      hasDiscount,
      displayPrice,
      formatPrice,
      handleImageError,
    };
  },
};
</script>

<style scoped>
.pro-card {
  flex-shrink: 0;
  width: 300px;
  scroll-snap-align: start;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.image-wrapper {
  aspect-ratio: 1 / 1.2;
  position: relative;
  background-color: #f3f3f3;
  border-radius: 4px;
  margin-bottom: 20px;

  /* Masquage strict pour que l'image ne déborde pas au zoom */
  overflow: hidden;

  /* Isolation 3D pour éviter les conflits avec l'animation v-scroll-reveal du parent */
  transform: translateZ(0);
  -webkit-mask-image: -webkit-radial-gradient(white, black);
  isolation: isolate;
}

.sale-badge {
  position: absolute;
  top: 16px;
  left: 16px;
  background-color: #ef4444;
  color: white;
  font-size: 10px;
  padding: 4px 8px;
  border-radius: 1px;
  font-weight: bold;
  text-transform: uppercase;
  z-index: 10;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;

  /* Préparation matérielle pour une animation fluide */
  will-change: transform;
  backface-visibility: hidden;

  /* Transition forcée (!important aide si Tailwind est utilisé) */
  transition: transform 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
}

/* LE DÉCLENCHEUR : Uniquement quand on survole le bloc de l'image */
.image-wrapper:hover .product-image {
  transform: scale(1.1) !important;
}

.product-info {
  font-family: 'Urbanist', sans-serif;
}

.product-name {
  font-weight: 500;
  color: #111827;
  margin: 0 0 4px 0;
  font-size: 16px;
  text-align: start;
}

.product-price {
  font-weight: 900;
  color: #111827;
  font-size: 20px;
  margin: 0;
}

.product-base-price {
  color: #6b7280;
  font-size: 14px;
  margin: 0 0 2px;
  text-decoration: line-through;
}
</style>
