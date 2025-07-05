<!-- frontend/src/views/AnalysisView.vue -->
<template>
  <div class="max-w-2xl mx-auto p-6 space-y-4">
    <h1 class="text-2xl font-bold">Contract Summary</h1>

    <div v-if="analysisResult && analysisResult.length">
      <ul class="space-y-2">
        <li v-for="(clause, idx) in analysisResult" :key="idx">
          <strong>{{ clause.title }}:</strong> {{ clause.summary }}
        </li>
      </ul>
    </div>
    <p v-else class="text-gray-500">No analysis data found. Please return to Home and analyze a contract first.</p>
  </div>
</template>

<script setup>
import { analysisResult } from '@/composables/useContractAnalysis'
</script>

<style scoped>
/* optional small tweaks */
</style>
