<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Document History</h1>
            <p class="mt-2 text-gray-600">View your uploaded documents and analysis results</p>
          </div>
          
          <!-- Summary Stats -->
          <div v-if="summary" class="flex space-x-6">
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600">{{ summary.total_documents }}</div>
              <div class="text-sm text-gray-500">Total Documents</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-green-600">{{ summary.documents_with_analysis }}</div>
              <div class="text-sm text-gray-500">Analyzed</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-orange-600">{{ summary.analysis_completion_rate.toFixed(1) }}%</div>
              <div class="text-sm text-gray-500">Completion Rate</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <span class="ml-3 text-gray-600">Loading your document history...</span>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
        <div class="flex items-center">
          <div class="text-red-600 mr-3">⚠️</div>
          <div>
            <h3 class="text-lg font-medium text-red-800">Error Loading History</h3>
            <p class="text-red-600 mt-1">{{ error }}</p>
          </div>
        </div>
        <button 
          @click="loadHistory" 
          class="mt-4 bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition-colors"
        >
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="documents.length === 0" class="text-center py-12">
        <div class="text-gray-400 text-6xl mb-4">📄</div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">No Documents Yet</h3>
        <p class="text-gray-600 mb-6">Upload your first document to get started with analysis</p>
        <router-link 
          to="/home" 
          class="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition-colors"
        >
          Upload Document
        </router-link>
      </div>

      <!-- Documents List -->
      <div v-else class="space-y-6">
        <div v-for="item in documents" :key="item.document.id" class="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow">
          <div class="p-6">
            <!-- Document Header -->
            <div class="flex justify-between items-start mb-4">
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900 mb-1">
                  {{ item.document.filename }}
                </h3>
                <p v-if="item.document.description" class="text-gray-600 text-sm mb-2">
                  {{ item.document.description }}
                </p>
                <div class="flex items-center space-x-4 text-sm text-gray-500">
                  <span>Document ID: {{ item.document.id }}</span>
                  <span class="flex items-center">
                    <div class="w-2 h-2 rounded-full mr-2" :class="item.has_analysis ? 'bg-green-500' : 'bg-orange-500'"></div>
                    {{ item.has_analysis ? 'Analysis Complete' : 'Pending Analysis' }}
                  </span>
                </div>
              </div>
              
              <!-- Actions -->
              <div class="flex space-x-2">
                <button 
                  @click="viewDocument(item.document.id)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  View Document
                </button>
                <button 
                  v-if="item.has_analysis"
                  @click="viewAnalysis(item.document.id)"
                  class="text-green-600 hover:text-green-800 text-sm font-medium"
                >
                  View Analysis
                </button>
              </div>
            </div>

            <!-- Analysis Results Preview -->
            <div v-if="item.has_analysis && item.analysis_results" class="bg-gray-50 rounded-md p-4">
              <h4 class="font-medium text-gray-900 mb-2">Analysis Summary</h4>
              <div class="text-sm text-gray-600">
                <!-- Display analysis results summary here -->
                <p v-if="item.analysis_results.summary">{{ item.analysis_results.summary }}</p>
                <p v-else>Analysis completed successfully</p>
              </div>
            </div>

            <!-- No Analysis State -->
            <div v-else class="bg-orange-50 rounded-md p-4">
              <div class="flex items-center">
                <div class="text-orange-600 mr-2">⏳</div>
                <div>
                  <h4 class="font-medium text-orange-800">Analysis Pending</h4>
                  <p class="text-sm text-orange-600">This document hasn't been analyzed yet</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Document Detail Modal -->
    <div v-if="selectedDocument" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div class="flex justify-between items-center p-6 border-b">
          <h2 class="text-xl font-semibold">{{ selectedDocument.filename }}</h2>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[70vh]">
          <pre class="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded-md">{{ JSON.stringify(selectedDocument.file, null, 2) }}</pre>
        </div>
      </div>
    </div>

    <!-- Analysis Detail Modal -->
    <div v-if="selectedAnalysis" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden">
        <div class="flex justify-between items-center p-6 border-b">
          <h2 class="text-xl font-semibold">Analysis Results</h2>
          <button @click="closeAnalysisModal" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[70vh]">
          <pre class="whitespace-pre-wrap text-sm text-gray-700 bg-gray-50 p-4 rounded-md">{{ JSON.stringify(selectedAnalysis, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { historyService } from '@/services'

export default {
  name: 'HistoryView',
  data() {
    return {
      documents: [],
      summary: null,
      loading: true,
      error: null,
      selectedDocument: null,
      selectedAnalysis: null
    }
  },
  async mounted() {
    await this.loadHistory()
    await this.loadSummary()
  },
  methods: {
    async loadHistory() {
      this.loading = true
      this.error = null
      
      try {
        const response = await historyService.getUserHistory()
        this.documents = response.documents || []
      } catch (error) {
        console.error('Error loading history:', error)
        this.error = error.response?.data?.error || 'Failed to load document history'
      } finally {
        this.loading = false
      }
    },
    
    async loadSummary() {
      try {
        this.summary = await historyService.getHistorySummary()
      } catch (error) {
        console.error('Error loading summary:', error)
      }
    },
    
    async viewDocument(documentId) {
      try {
        const response = await historyService.getDocumentHistory(documentId)
        this.selectedDocument = response.document
      } catch (error) {
        console.error('Error loading document:', error)
        this.error = 'Failed to load document details'
      }
    },
    
    async viewAnalysis(documentId) {
      try {
        const response = await historyService.getDocumentAnalysis(documentId)
        this.selectedAnalysis = response.analysis_results
      } catch (error) {
        console.error('Error loading analysis:', error)
        this.error = 'Failed to load analysis results'
      }
    },
    
    closeModal() {
      this.selectedDocument = null
    },
    
    closeAnalysisModal() {
      this.selectedAnalysis = null
    }
  }
}
</script>

<style scoped>
/* Add any additional custom styles here */
</style>
