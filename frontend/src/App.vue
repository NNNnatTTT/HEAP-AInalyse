<script setup>
import Navbar from './components/NavBar.vue'
</script>

<template>
  <div id="app" class="flex flex-col min-h-screen overflow-x-hidden">
    <!-- Navbar always visible -->
    <Navbar />

    <!-- Page content area -->
    <main class="flex-1 w-full">
      <router-view />
    </main>
  </div>
</template>

<!-- No scoped styling needed, Tailwind handles layout -->
<style>
/* Global safety net (optional, can go in main.css too) */
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100vw;
  overflow-x: hidden;
}

* {
  box-sizing: border-box;
}
</style>
