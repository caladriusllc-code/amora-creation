<template>
  <header
    class="site-header"
    :class="[
      `theme--${theme}`,
      {
        'header--hidden': !showHeader,
        'header--transparent': theme === 'transparent' && isAtTop && !isMenuOpen && !isSearchOpen,
        'header--solid': theme === 'transparent' && (!isAtTop || isMenuOpen || isSearchOpen)
      }
    ]"
  >
    <div class="top-bar">
      <p>DECOUVREZ VOTRE BOUTIQUE DE MODE AFRICAINE</p>
    </div>

    <nav class="main-nav">
      <div class="logo" @click="()=>{router.push('/')}">Amora.</div>

      <ul class="nav-links">
        <li><NuxtLink to="/" :class="{ 'active-link': isNavLinkActive('/') }">Accueil</NuxtLink></li>
        <li><NuxtLink to="/collection" :class="{ 'active-link': isNavLinkActive('/collection') }">Collection</NuxtLink></li>
        <li><NuxtLink to="/categories" :class="{ 'active-link': isNavLinkActive('/categories') }">Categories</NuxtLink></li>
        <li><NuxtLink to="/soldes" :class="{ 'active-link': isNavLinkActive('/soldes') }">Soldes</NuxtLink></li>
        <li><NuxtLink to="/about" :class="{ 'active-link': isNavLinkActive('/about') }">A propos</NuxtLink></li>
      </ul>

      <div class="nav-actions">
        <!-- ⚡️ CORRECTION : L'input desktop a maintenant toutes ses props -->
        <div class="desktop-search">
          <BaseResearchInput
            placeholder="Que recherchez-vous ?"
            v-model="query"
            :results="productStore.searchResults"
            :isLoading="productStore.isSearching"
            @search="handleSearch"
            @clear="clearSearch"
            @select="goToProduct"
          />
        </div>

        <button class="mobile-search-toggle" @click="toggleSearch" aria-label="Rechercher">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
        </button>

        <cart-button
          :badgeCount="cartStore.totalItems"
          @click="()=>$emit('toggle-cart')"
        />

        <button class="hamburger" @click="toggleMenu" aria-label="Menu" :class="{ 'is-active': isMenuOpen }">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    </nav>

    <!-- ⚡️ CORRECTION : L'input mobile est corrigé (plus de @select vide) -->
    <transition name="menu-slide">
      <div v-if="isSearchOpen" class="mobile-search-dropdown">
        <BaseResearchInput
            placeholder="Que recherchez-vous ?"
            v-model="query"
            :results="productStore.searchResults"
            :isLoading="productStore.isSearching"
            @search="handleSearch"
            @clear="clearSearch"
            @select="goToProduct"
        />
      </div>
    </transition>

    <transition name="menu-slide">
      <div v-if="isMenuOpen" class="mobile-menu">
        <ul class="mobile-nav-links">
          <li @click="closeMenu"><NuxtLink to="/collection" :class="{ 'active-link': isNavLinkActive('/collection') }">Collection</NuxtLink></li>
          <li @click="closeMenu"><NuxtLink to="/categories" :class="{ 'active-link': isNavLinkActive('/categories') }">Categories</NuxtLink></li>
          <li @click="closeMenu"><NuxtLink to="/soldes" :class="{ 'active-link': isNavLinkActive('/soldes') }">Soldes</NuxtLink></li>
          <li @click="closeMenu"><NuxtLink to="/tendances" :class="{ 'active-link': isNavLinkActive('/tendances') }">A propos</NuxtLink></li>
        </ul>
      </div>
    </transition>
  </header>
</template>

<script lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import { useCartStore } from '../../stores/cartStore'
import { useProductStore } from '~/stores/productStore';
import cartButton from '../buttons/cartButton.vue';
import BaseResearchInput from '../input/BaseResarchInput.vue';

export default {
  components: { cartButton, BaseResearchInput },
  props: {
    theme: {
      type: String,
      default: 'transparent',
    }
  },

  emits: ['toggle-cart'],

  setup() {
    const cartStore = useCartStore();
    const productStore = useProductStore();
    const route = useRoute();
    const router = useRouter();

    const isMenuOpen = ref(false);
    const isSearchOpen = ref(false);
    const query = ref('');
    let debounceTimeout: ReturnType<typeof setTimeout> | null = null;

    // ⚡️ CORRECTION : Ajout du délai 300ms et sécurisation du paramètre
    const handleSearch = (searchQuery: string) => {
      if (debounceTimeout) clearTimeout(debounceTimeout)

      if (typeof searchQuery !== 'string' || !searchQuery.trim()) {
        productStore.searchResults = [];
        return;
      }

      // Attends 300ms après la saisie de l'utilisateur
      debounceTimeout = setTimeout(() => {
        productStore.searchProducts(searchQuery)
      }, 300) // Le fameux 300 manquant !
    }

    // ⚡️ NOUVEAU : Fonction propre pour nettoyer la recherche
    const clearSearch = () => {
      query.value = '';
      productStore.searchResults = [];
    }

    // ⚡️ NOUVEAU : Gère le clic sur un résultat de recherche
    const goToProduct = (product: any) => {
      if (product && product.slug) {
        router.push(`/product/${product.slug}`);
        clearSearch();
        isSearchOpen.value = false;
      }
    }

    const toggleMenu = () => {
      isMenuOpen.value = !isMenuOpen.value;
      if (isMenuOpen.value) isSearchOpen.value = false;
    };

    const toggleSearch = () => {
      isSearchOpen.value = !isSearchOpen.value;
      if (isSearchOpen.value) isMenuOpen.value = false;
    };

    const closeMenu = () => isMenuOpen.value = false;

    const isNavLinkActive = (path: string) => {
      if (path === '/') return route.path === '/';
      return route.path === path || route.path.startsWith(`${path}/`);
    };

    const showHeader = ref(true);
    const isAtTop = ref(true);
    let lastScrollPosition = 0;

    const handleScroll = () => {
      const currentScrollPosition = window.scrollY;
      isAtTop.value = currentScrollPosition < 50;

      if (currentScrollPosition > lastScrollPosition && currentScrollPosition > 100) {
        showHeader.value = false;
        isMenuOpen.value = false;
        isSearchOpen.value = false;
      } else {
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
      debounceTimeout,
      handleSearch,
      clearSearch,
      goToProduct,
      productStore,
      cartStore,
      isNavLinkActive,
      router,
      isMenuOpen,
      toggleMenu,
      query,
      closeMenu,
      isSearchOpen,
      toggleSearch,
      showHeader,
      isAtTop
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

/* ======= THEMES DYNAMIQUES ======= */

/* 1. Theme Transparent (Par défaut) */
.header--transparent .main-nav {
  background: transparent;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
}
.header--transparent .logo,
.header--transparent .nav-links li a,
.header--transparent .top-bar-link { color: #ffffff; }
.header--transparent .hamburger span { background: #ffffff; }
.header--transparent .mobile-search-toggle svg { stroke: #ffffff; }

/* 2. Theme Light (Fond blanc, texte noir) - Activé au scroll ou via theme="light" */
.header--solid .main-nav,
.theme--light .main-nav {
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
.header--solid .logo,
.header--solid .nav-links li a,
.theme--light .logo,
.theme--light .nav-links li a { color: #000000; }
.header--solid .hamburger span,
.theme--light .hamburger span { background: #000000; }
.header--solid .mobile-search-toggle svg,
.theme--light .mobile-search-toggle svg { stroke: #000000; }

/* 3. Theme Dark (Fond noir, texte blanc) - Activé via theme="dark" */
.theme--dark .main-nav {
  background: rgba(0, 0, 0, 0.98);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 4px 6px -1px rgba(255, 255, 255, 0.05);
}
.theme--dark .logo,
.theme--dark .nav-links li a { color: #ffffff; }
.theme--dark .hamburger span { background: #ffffff; }
.theme--dark .mobile-search-toggle svg { stroke: #ffffff; }
/* Inversion de la top bar pour le thème sombre */
.theme--dark .top-bar { background-color: #ffffff; color: #000000; }
.theme--dark .top-bar-link { color: #000000; }


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
  width: 100%;
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
  cursor: pointer;
}

.nav-links { display: flex; list-style: none; gap: 32px; font-size: 14px; text-transform: uppercase; font-weight: 600;}
.nav-links li a { transition: color 0.4s ease; cursor: pointer; text-decoration: none; }
.nav-actions { display: flex; align-items: center; gap: 20px; }

/* Desktop Search */
.desktop-search {
  width: 250px;
}

/* Mobile Search Toggle Button */
.mobile-search-toggle {
  display: none;
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

/* Menus déroulants Mobiles (Gère l'adaptation au thème sombre) */
.mobile-search-dropdown,
.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  padding: 1rem 1.5rem;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  z-index: 49;
  box-sizing: border-box;
  border-top: 1px solid #f0f0f0;
}
.mobile-nav-links { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 16px; }
.mobile-nav-links li { font-size: 16px; font-weight: 500; text-transform: uppercase; color: #4b5563; padding: 8px 0; border-bottom: 1px solid #f0f0f0; cursor: pointer; }
.mobile-nav-links li a { text-decoration: none; color: inherit; display: block; }

/* Ajustements pour le thème dark sur le menu mobile */
.theme--dark .mobile-search-dropdown,
.theme--dark .mobile-menu {
  background: #000000;
  border-top: 1px solid #333;
}
.theme--dark .mobile-nav-links li {
  color: #ffffff;
  border-bottom: 1px solid #333;
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

/* Animations menu slide */
.menu-slide-enter-active,
.menu-slide-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.menu-slide-enter-from,
.menu-slide-leave-to { opacity: 0; transform: translateY(-20px); }

/* ===== ACTIVE LINK INDICATOR ===== */

/* Base active-link style (underline) */
.nav-links li a.active-link {
  position: relative;
  text-decoration: none;
}
.nav-links li a.active-link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: currentColor;
  transition: transform 0.3s ease;
}

/* Theme‑specific active link colors */
.header--transparent .nav-links li a.active-link {
  color: #ffffff;
}
.header--transparent .nav-links li a.active-link::after {
  background-color: #ffffff;
}

.header--solid .nav-links li a.active-link,
.theme--light .nav-links li a.active-link {
  color: #000000;
}
.header--solid .nav-links li a.active-link::after,
.theme--light .nav-links li a.active-link::after {
  background-color: #000000;
}

.theme--dark .nav-links li a.active-link {
  color: #ffffff;
}
.theme--dark .nav-links li a.active-link::after {
  background-color: #ffffff;
}

/* Mobile menu active link */
.mobile-nav-links li a.active-link {
  color: #000000 !important;
  font-weight: 700;
  border-bottom: 2px solid #000000;
}
.theme--dark .mobile-nav-links li a.active-link {
  color: #ffffff !important;
  border-bottom-color: #ffffff;
}

/* ==== MEDIA QUERY MOBILE ==== */
@media (max-width: 768px) {
  .nav-links, .desktop-search { display: none; }
  .hamburger, .mobile-search-toggle { display: flex; }
  .mobile-nav-links li { font-weight: 600; }
}
</style>
