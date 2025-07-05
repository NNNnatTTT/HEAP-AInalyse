import axios from 'axios'

export async function parsePdf(file) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await axios.post('/scan_document', form)
  return data.pages
}

export async function analyseContract(pages, prompt) {
  const { data } = await axios.post('/api/ai/analyse', { pages, prompt })
  return data
}

// composables/useContractAnalysis.js
import { ref } from 'vue'
export const analysisResult = ref(null)

export function setAnalysisResult(r) {
  analysisResult.value = r
}
