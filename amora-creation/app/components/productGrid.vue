<template>
  <section class="product-section">
    <div class="section-header">
      <h2 class="section-title">Featured products</h2>
      <div class="slider-controls">
        <button class="control-btn">&larr;</button>
        <button class="control-btn">&rarr;</button>
      </div>
    </div>
    
    <div class="grid">
      <div v-for="product in products" :key="product.id" class="product-card">
        <div class="image-wrapper">
          <span v-if="product.sale" class="sale-badge">Sale</span>
          <img :src="product.image" :alt="product.name" class="product-image" />
        </div>
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-price">{{ formatPrice(product.price) }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { ref } from 'vue';

// Typage strict des données pour l'API
interface Product {
  id: number;
  name: string;
  price: number;
  image: string;
  sale: boolean;
}

export default {
  setup() {
    const products = ref<Product[]>([
      { 
        id: 1, 
        name: 'Robe d\'Automne', 
        price: 35000, 
        image: 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600&q=80', 
        sale: false 
      },
      { 
        id: 2, 
        name: 'Chemise Grise', 
        price: 25000, 
        image: 'https://images.unsplash.com/photo-1586363104862-3a5e2ab60d99?w=600&q=80', 
        sale: false 
      },
      { 
        id: 3, 
        name: 'Manteau en Cuir', 
        price: 65000, 
        image: 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600&q=80', 
        sale: true 
      },
      { 
        id: 4, 
        name: 'Foulard en Soie', 
        price: 15000, 
        image: 'https://images.unsplash.com/photo-1584916201218-f4242ceb4809?w=600&q=80', 
        sale: false 
      },
    ]);

    const formatPrice = (amount: number): string => {
      return new Intl.NumberFormat('fr-FR', { 
        style: 'currency', 
        currency: 'XOF',
        maximumFractionDigits: 0
      }).format(amount);
    };

    return { 
      products,
      formatPrice
    };
  }
}
</script>

<style scoped>
.product-section {
  max-width: 1280px;
  margin: 0 auto;
  padding: 64px 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
  font-family: 'Urbanist', sans-serif;
}

.section-title {
  font-size: 30px;
  font-weight: 700;
  text-transform: uppercase;
  margin: 0;
}

.slider-controls {
  display: flex;
  gap: 8px;
}

.control-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #e5e7eb;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  transition: all 0.3s ease;
}

.control-btn:hover {
  background: #000;
  color: #fff;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 32px;
}

.product-card {
  cursor: pointer;
}

.image-wrapper {
  position: relative;
  aspect-ratio: 3/4;
  background-color: #f3f3f3;
  border-radius: 16px;
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
  border-radius: 4px;
  font-weight: bold;
  text-transform: uppercase;
  z-index: 10;
  font-family: 'Inter', sans-serif;
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