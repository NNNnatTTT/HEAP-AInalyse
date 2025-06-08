<script setup>
import Navbar from './components/NavBar.vue'
</script>

<template>
  <div id="app">
    <Navbar></Navbar>
    <!-- This is crucial - without router-view, your pages won't display -->
    <router-view></router-view>
  </div>
</template>
