<template>
  <header 
    class="site-header" 
    :class="{ 
      'header--hidden': !showHeader, 
      'header--transparent': isAtTop && !isMenuOpen && !isSearchOpen, 
      'header--solid': !isAtTop || isMenuOpen || isSearchOpen
    }"
  >
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
        <div class="desktop-search">
          <BaseResearchInput />
        </div>

        <button class="mobile-search-toggle" @click="toggleSearch" aria-label="Rechercher">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
        </button>

        <cart-button />
        
        <button class="hamburger" @click="toggleMenu" aria-label="Menu" :class="{ 'is-active': isMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>

    <transition name="menu-slide">
      <div v-if="isSearchOpen" class="mobile-search-dropdown">
        <BaseResearchInput placeholder="Que recherchez-vous ?" v-model="query"/>
      </div>
    </transition>

    <transition name="menu-slide">
      <div v-if="isMenuOpen" class="mobile-menu">
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
import { ref, onMounted, onUnmounted } from 'vue';
import cartButton from '../buttons/cartButton.vue';
import BaseResearchInput from '../input/BaseResarchInput.vue';

export default {
  components: { cartButton, BaseResearchInput },
  setup() {
    const isMenuOpen = ref(false);
    const isSearchOpen = ref(false); // Nouvelle variable pour la recherche mobile
    const query = ref('')

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
      if (isMenuOpen.value) isSearchOpen.value = false; // Ferme la recherche si on ouvre le menu
    };

    const toggleSearch = () => {
      isSearchOpen.value = !isSearchOpen.value;
      if (isSearchOpen.value) isMenuOpen.value = false; // Ferme le menu si on ouvre la recherche
    };

    const closeMenu = () => isMenuOpen.value = false;
    
    // --- VARIABLES POUR LE SCROLL ---
    const showHeader = ref(true); 
    const isAtTop = ref(true);   
    let lastScrollPosition = 0;  

    const handleScroll = () => {
      const currentScrollPosition = window.scrollY;

      isAtTop.value = currentScrollPosition < 50;

      if (currentScrollPosition > lastScrollPosition && currentScrollPosition > 100) {
        // On descend : on cache la nav et on referme les menus ouverts
        showHeader.value = false;
        isMenuOpen.value = false;
        isSearchOpen.value = false;
      } else {
        // On monte : on affiche la nav
        showHeader.value = true;
      }

      lastScrollPosition = currentScrollPosition;
    };

    onMounted(() => {
      window.addEventListener('scroll', handleScroll);
    });

    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll);
    });

    return { 
      isMenuOpen, toggleMenu, query, closeMenu, 
      isSearchOpen, toggleSearch,
      showHeader, isAtTop 
    };
  }
}
</script>

<style scoped>
/* ======= Base ======= */
.site-header {
  width: 100%;
  position: fixed; 
  top: 0;
  z-index: 50;
  transition: transform 0.4s ease-in-out, background-color 0.4s ease;
}

.header--hidden {
  transform: translateY(-100%);
}

.header--transparent .main-nav {
  background: transparent;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
}
.header--transparent .logo,
.header--transparent .nav-links li {
  color: #ffffff;
}
.header--transparent .hamburger span {
  background: #ffffff;
}
.header--transparent .top-bar-link {
  color: #ffffff;
}
.header--transparent .mobile-search-toggle svg {
  stroke: #ffffff;
}

.header--solid .main-nav {
  width: 100%;
  background: rgba(255, 255, 255, 0.98); 
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.header--solid .logo,
.header--solid .nav-links li {
  color: #000000;
}
.header--solid .hamburger span {
  background: #000000;
}
.header--solid .mobile-search-toggle svg {
  stroke: #000000;
}

/* ======= Styles restants ======= */
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
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.4s ease; 
}

.logo {
  font-size: 24px;
  font-weight: 900;
  font-family: 'Urbanist', sans-serif;
  text-transform: uppercase;
  transition: color 0.4s ease;
}

.nav-links { display: flex; list-style: none; gap: 32px; font-size: 14px; text-transform: uppercase; font-weight: 600;}
.nav-links li { transition: color 0.4s ease; cursor: pointer; }
.nav-actions { display: flex; align-items: center; gap: 20px; }

/* Desktop Search */
.desktop-search {
  width: 250px;
}

/* Mobile Search Toggle Button */
.mobile-search-toggle {
  display: none; /* Caché sur ordinateur */
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
}
.mobile-search-toggle svg {
  width: 100%;
  height: 100%;
  transition: stroke 0.4s ease;
}

/* Mobile Search Dropdown */
.mobile-search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  padding: 1rem 1.5rem;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  z-index: 48;
  box-sizing: border-box;
  border-top: 1px solid #f0f0f0;
}

/* Hamburger Menu */
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
.hamburger span { width: 100%; height: 2px; transition: all 0.3s ease; }
.hamburger.is-active span:nth-child(1) { transform: translateY(6px) rotate(45deg); }
.hamburger.is-active span:nth-child(2) { opacity: 0; }
.hamburger.is-active span:nth-child(3) { transform: translateY(-6px) rotate(-45deg); }

/* Menu Mobile Styles */
.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  padding: 1.5rem;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  z-index: 49;
  box-sizing: border-box; 
}
.mobile-nav-links { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 16px; }
.mobile-nav-links li { font-size: 16px; font-weight: 500; text-transform: uppercase; color: #4b5563; padding: 8px 0; border-bottom: 1px solid #f0f0f0; cursor: pointer; }

/* Animations menu slide */
.menu-slide-enter-active,
.menu-slide-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.menu-slide-enter-from,
.menu-slide-leave-to { opacity: 0; transform: translateY(-20px); }

/* ==== MEDIA QUERY MOBILE ==== */
@media (max-width: 768px) {
  .nav-links, .desktop-search { display: none; }
  .hamburger, .mobile-search-toggle { display: flex; }
  .mobile-nav-links li { font-weight: 600; }
}
</style>