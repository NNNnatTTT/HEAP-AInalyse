<!-- frontend/src/views/AnalysisView.vue -->
<template>
  <div class="max-w-3xl mx-auto p-6 space-y-6">
    <header class="text-center space-y-2">
      <h1 class="text-3xl font-bold text-gray-800">Contract Analysis Summary</h1>
      <p class="text-gray-600">Review key insights from your contract</p>
    </header>

    <div v-if="analysisResult && analysisResult.length" class="grid gap-6">
      <div 
        v-for="(clause, idx) in analysisResult" 
        :key="idx" 
        class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300"
      >
        <h2 class="text-xl font-semibold text-blue-600 mb-4 border-b-2 border-blue-200 pb-2">{{ clause.title }}</h2>
        <p class="text-gray-700 mb-4">{{ clause.summary }}</p>
        <div v-if="clause.action" class="bg-yellow-50 p-3 rounded-md border-l-4 border-yellow-400">
          <p class="text-sm font-medium text-yellow-800">Action: {{ clause.action }}</p>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12 bg-gray-50 rounded-lg">
      <p class="text-gray-500 mb-4">No analysis data found.</p>
      <RouterLink 
        to="/" 
        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
      >
        <span>Analyze a Contract</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { analysisResult } from '@/composables/useContractAnalysis'
import { RouterLink } from 'vue-router'
</script>

<style scoped>
/* Smooth transition for hover effects */
.router-link-active {
  @apply bg-blue-700;
}
</style>