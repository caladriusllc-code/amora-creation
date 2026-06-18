<template>
  <header class="site-header">
    <div class="top-bar">
      Sign up and get 20% off to your first order. <a href="#" class="top-bar-link">Sign up now</a>
    </div>
    
    <nav class="main-nav">
      <div class="logo">Amora.</div>
      
      <ul class="nav-links">
        <li class="active">Shop</li>
        <li>Most Wanted</li>
        <li>New Arrivals</li>
        <li>Brands</li>
      </ul>

      <div class="nav-actions">
        <div class="search-box">
          <input type="text" placeholder="Search" />
        </div>
        <cart-button />
        <button class="hamburger" @click="toggleMenu" aria-label="Menu" :class="{ 'is-active': isMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>

    <transition name="menu-slide">
      <div v-if="isMenuOpen" class="mobile-menu">
        <div class="mobile-search">
          <input type="text" placeholder="Search" />
        </div>
        <ul class="mobile-nav-links">
          <li class="active" @click="closeMenu">Shop</li>
          <li @click="closeMenu">Most Wanted</li>
          <li @click="closeMenu">New Arrivals</li>
          <li @click="closeMenu">Brands</li>
        </ul>
      </div>
    </transition>
  </header>
</template>

<script lang="ts">
import { ref } from 'vue';
import cartButton from './buttons/cartButton.vue';

export default {
  components:{ cartButton },
  setup() {
    const isMenuOpen = ref(false);
    const toggleMenu = () => isMenuOpen.value = !isMenuOpen.value;
    const closeMenu = () => isMenuOpen.value = false;
    
    return { isMenuOpen, toggleMenu, closeMenu };
  }
}
</script>

<style scoped>
/* ======= Base (Inchangé mais vérifié) ======= */
.site-header {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 50;
  /* On ne met PAS d'overflow-x hidden ici */
}

.top-bar {
  background-color: #000;
  color: #fff;
  font-size: 11px;
  padding: 8px;
  text-align: center;
  font-family: 'Inter', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.main-nav {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(238, 238, 238, 0.5);
}

.logo {
  font-size: 24px;
  font-weight: 900;
  font-family: 'Urbanist', sans-serif;
  text-transform: uppercase;
}

/* ======= Menu Mobile Styles ======= */
.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  padding: 1.5rem;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  z-index: 49;
  /* On s'assure que le menu ne peut pas être scrollé horizontalement */
  box-sizing: border-box; 
}

/* ======= CLASSES DE TRANSITION VUE ======= */
/* "menu-slide" correspond au name="menu-slide" dans le <transition> */

.menu-slide-enter-active,
.menu-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.menu-slide-enter-from,
.menu-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px); /* Le menu remonte un peu et disparaît */
}

/* ======= Hamburger Animation (Bonus) ======= */
.hamburger {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 20px;
  height: 14px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.hamburger span {
  width: 100%;
  height: 2px;
  background: #000;
  transition: all 0.3s;
}

/* Transforme le hamburger en X quand le menu est ouvert */
.hamburger.is-active span:nth-child(1) {
  transform: translateY(6px) rotate(45deg);
}
.hamburger.is-active span:nth-child(2) {
  opacity: 0;
}
.hamburger.is-active span:nth-child(3) {
  transform: translateY(-6px) rotate(-45deg);
}

/* ======= Desktop & Utils ======= */
.nav-links { display: flex; list-style: none; gap: 32px; font-size: 14px; text-transform: uppercase; }
.nav-actions { display: flex; align-items: center; gap: 20px; }
.search-box input { background: #f3f4f6; border: none; padding: 8px 16px; border-radius: 999px; font-size: 12px; }

.mobile-nav-links { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 16px; }
.mobile-nav-links li { font-size: 16px; text-transform: uppercase; color: #4b5563; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }

@media (max-width: 768px) {
  .nav-links, .search-box { display: none; }
  .hamburger { display: flex; }
}
</style>