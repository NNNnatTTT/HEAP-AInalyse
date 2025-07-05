<template>
  <nav class="bg-white shadow-md px-6 py-4 flex justify-between items-center">
    <div class="text-xl font-bold text-gray-800">AInalyse</div>
    <ul class="flex space-x-6">
      <li><router-link to="/home" class="text-gray-700 hover:text-blue-600">Home</router-link></li>
      <li><router-link to="/compare" class="text-gray-700 hover:text-blue-600">Compare</router-link></li>
      <li><router-link to="/about" class="text-gray-700 hover:text-blue-600">About</router-link></li>
    </ul>
  </nav>
</template>

<script setup>
// No logic needed here unless you're handling active route programmatically
</script>

.container {
  max-width: 100%;
  overflow-x: hidden;
}
