<template>
  <div class="p-4">
    <input type="file" @change="onFile" accept="application/pdf" />
    <button :disabled="!file" @click="runAnalysis">Analyse</button>
    <pre v-if="result">{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { parsePdf, analyseContract } from '@/composables/useContractAnalysis'

const file   = ref(null)
const result = ref('')

function onFile(e) {
  file.value = e.target.files[0]
}

async function runAnalysis() {
  const pages = await parsePdf(file.value)
  const ai    = await analyseContract(
    pages,
    'Highlight key risk clauses and summarize obligations.'
  )
  result.value = JSON.stringify(ai, null, 2)
}
</script>
