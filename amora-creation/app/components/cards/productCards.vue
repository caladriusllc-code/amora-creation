<template>
    <div class="pro-card">
        <div class="image-wrapper" @click="$emit('goToProductDetail')">
          <span v-if="sale" class="sale-badge">Sale</span>
          <img :src="image" :alt="name" class="product-image" />
        </div>
        <div class="card-footer w-full flex flex-row items-center justify-between">
            <div class="product-info">
                <h3 class="product-name">{{ name }}</h3>
                <p class="product-price">{{ formatPrice(price) }}</p>
            </div>
            <cart-button 
                @click="$emit('addToCart')"
                :isLoading="isLoading"
            />
        </div>
      </div>
</template>

<script>
import cartButton from '../buttons/cartButton.vue';
import { useCartStore } from '../../stores/cartStore'
export default {
    name: 'productCards',
    components:{
        cartButton
    },
    props:{
        image: String,
        name: String,
        price: Number,
        sale: Boolean,
        isLoading: Boolean
    },
    emits: ['addToCart', 'goToProductDetail'],
    setup(props) {

        const cartStore = useCartStore();
        
        const formatPrice = (amount) => {
          return new Intl.NumberFormat('fr-FR', { 
            style: 'currency', 
            currency: 'XOF',
            maximumFractionDigits: 0
          }).format(amount || 0);
        };

        console.log('ProductCards - Image prop reçue:', props.image);

        const handleImageError = (e) => {
            console.error('Erreur chargement image:', props.image, e);
            e.target.src = 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80';
        };

        return {
          cartStore,
          formatPrice,
          handleImageError
        };
    }
}
</script>

<style scoped>
    .pro-card {
    flex-shrink: 0;
    width: 280px;
    scroll-snap-align: start;
    cursor: pointer;
    transition: transform 0.3s ease;
    }

    .pro-card:hover {
    transform: translateY(-4px);
    }

    .image-wrapper {
    aspect-ratio: 1 / 1;
    position: relative;
    background-color: #f3f3f3;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 16px;
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
    transition: transform 0.5s ease;
    }

    .product-card:hover .product-image {
    transform: scale(1.05);
    }

    .product-info {
    font-family: 'Urbanist', sans-serif;
    }

    .product-name {
    font-weight: 700;
    color: #111827;
    margin: 0 0 4px 0;
    font-size: 16px;
    }

    .product-price {
    font-weight: 900;
    color: #111827;
    font-size: 18px;
    margin: 0;
    }

</style>