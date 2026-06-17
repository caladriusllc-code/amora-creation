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
        <button class="icon-btn">Panier</button>
      </div>
    </nav>
  </header>
</template>

<script lang="ts">
export default {
  setup() {
    // Logique du header (ex: gestion du scroll ou du panier) à venir
    return {};
  }
}
</script>

<style scoped>
.site-header {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 50;
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

.top-bar-link {
  text-decoration: underline;
  font-weight: bold;
  color: #fff;
}

.main-nav {
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  /* Effet Glassmorphism */
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
  letter-spacing: -1px;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 32px;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  color: #4b5563;
  text-transform: uppercase;
}

.nav-links li {
  cursor: pointer;
  transition: color 0.3s;
}

.nav-links li:hover, .nav-links li.active {
  color: #000;
}

.nav-links li.active {
  text-decoration: underline;
  text-underline-offset: 4px;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-box input {
  background: #f3f4f6;
  border: none;
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 12px;
  outline: none;
  font-family: 'Inter', sans-serif;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
}
</style>