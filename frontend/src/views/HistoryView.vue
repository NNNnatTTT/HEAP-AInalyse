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
          
          <!-- Summary Stats and Actions -->
          <div class="flex items-center space-x-6">
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
                <div class="text-2xl font-bold text-orange-600">{{ Math.round(summary.analysis_completion_rate) }}%</div>
                <div class="text-sm text-gray-500">Completion Rate</div>
              </div>
            </div>
            
            <!-- Batch Analysis Button -->
            <button 
              v-if="summary && summary.documents_without_analysis > 0"
              @click="triggerBatchAnalysis"
              :disabled="batchAnalyzing"
              class="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <svg v-if="batchAnalyzing" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 718-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ batchAnalyzing ? 'Analyzing...' : `Analyze All (${summary.documents_without_analysis})` }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Batch Analysis Progress Bar -->
    <div v-if="batchAnalyzing || batchProgress.show" class="bg-blue-50 border-b border-blue-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-lg font-medium text-blue-900">Batch Analysis Progress</h3>
          <div class="text-sm text-blue-700">
            {{ batchProgress.completed }} of {{ batchProgress.total }} documents analyzed
          </div>
        </div>
        
        <!-- Progress Bar -->
        <div class="w-full bg-blue-200 rounded-full h-3 mb-2">
          <div 
            class="bg-blue-600 h-3 rounded-full transition-all duration-500 ease-out"
            :style="{ width: batchProgress.percentage + '%' }"
          ></div>
        </div>
        
        <!-- Progress Details -->
        <div class="flex justify-between text-sm text-blue-700">
          <span>{{ batchProgress.percentage.toFixed(1) }}% Complete</span>
          <span v-if="batchProgress.estimatedTimeRemaining">
            Est. {{ batchProgress.estimatedTimeRemaining }} remaining
          </span>
        </div>
        
        <!-- Recently Completed Documents -->
        <div v-if="batchProgress.recentlyCompleted.length > 0" class="mt-3">
          <div class="text-sm text-blue-700 mb-1">Recently Completed:</div>
          <div class="flex flex-wrap gap-2">
            <div 
              v-for="doc in batchProgress.recentlyCompleted.slice(-5)" 
              :key="doc.id"
              class="bg-green-100 text-green-800 px-2 py-1 rounded text-xs"
            >
              {{ truncateText(doc.filename, 30) }} ✓
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
                  <!-- Batch Analysis Indicator -->
                  <span v-if="batchAnalyzing && !item.has_analysis" class="ml-2 inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    <svg class="animate-spin -ml-1 mr-1 h-3 w-3 text-purple-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 718-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </span>
                </h3>
                <p v-if="item.document.description" class="text-gray-600 text-sm mb-2">
                  {{ item.document.description }}
                </p>
                <div class="flex items-center space-x-4 text-sm text-gray-500">
                  <span class="flex items-center">
                    <div class="w-2 h-2 rounded-full mr-2" :class="item.has_analysis ? 'bg-green-500' : 'bg-orange-500'"></div>
                    {{ item.has_analysis ? 'Analysis Complete' : 'Pending Analysis' }}
                  </span>
                </div>
              </div>
              
              <!-- Actions -->
              <div class="flex space-x-2">
                <button 
                  @click="viewDocument(item)"
                  class="text-blue-600 hover:text-blue-800 text-sm font-medium px-3 py-1 rounded border border-blue-200 hover:bg-blue-50"
                >
                  View Document
                </button>
                <button 
                  v-if="item.has_analysis"
                  @click="viewAnalysis(item)"
                  class="text-green-600 hover:text-green-800 text-sm font-medium px-3 py-1 rounded border border-green-200 hover:bg-green-50"
                >
                  View Analysis
                </button>
                <button 
                  v-if="!item.has_analysis"
                  @click="analyzeDocument(item.document.id)"
                  :disabled="analyzingDocs.includes(item.document.id) || batchAnalyzing"
                  class="text-purple-600 hover:text-purple-800 text-sm font-medium px-3 py-1 rounded border border-purple-200 hover:bg-purple-50 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
                >
                  <svg v-if="analyzingDocs.includes(item.document.id)" class="animate-spin -ml-1 mr-1 h-3 w-3 text-purple-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 718-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ analyzingDocs.includes(item.document.id) ? 'Analyzing...' : 'Analyze' }}
                </button>
              </div>
            </div>

            <!-- No Analysis State -->
            <div v-if="!item.has_analysis" class="bg-orange-50 rounded-md p-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="text-orange-600 mr-2">⏳</div>
                  <div>
                    <h4 class="font-medium text-orange-800">Analysis Pending</h4>
                    <p class="text-sm text-orange-600">This document hasn't been analyzed yet</p>
                  </div>
                </div>
                <button 
                  @click="analyzeDocument(item.document.id)"
                  :disabled="analyzingDocs.includes(item.document.id) || batchAnalyzing"
                  class="bg-orange-600 text-white px-3 py-1 rounded text-sm hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ analyzingDocs.includes(item.document.id) ? 'Analyzing...' : 'Analyze Now' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Document Detail Modal with Pagination -->
    <div v-if="selectedDocument" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="closeModal">
      <div class="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-hidden" @click.stop>
        <div class="flex justify-between items-center p-6 border-b">
          <h2 class="text-xl font-semibold">{{ selectedDocument.filename }}</h2>
          <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto max-h-[70vh]">
          <div class="space-y-6">
            <!-- Document Information -->
            <div>
              <h3 class="font-medium text-gray-900 mb-2">Document Information</h3>
              <div class="bg-gray-50 p-4 rounded-md text-sm">
                <p><strong>Filename:</strong> {{ selectedDocument.filename }}</p>
                <p><strong>Description:</strong> {{ selectedDocument.description || 'No description' }}</p>
              </div>
            </div>
            
            <!-- Paginated Document Content -->
            <div v-if="getFileInfo(selectedDocument.file) && getFileInfo(selectedDocument.file).text">
              <div class="flex justify-between items-center mb-4">
                <h3 class="font-medium text-gray-900">Document Content</h3>
                <div v-if="documentPages.length > 1" class="text-sm text-gray-600">
                  {{ documentPages.length }} pages total
                </div>
              </div>
              
              <!-- Page Navigation (if multiple pages) -->
              <div v-if="documentPages.length > 1" class="flex justify-center items-center space-x-4 mb-4">
                <button 
                  @click="previousPage" 
                  :disabled="currentPage === 0"
                  class="px-3 py-1 bg-blue-600 text-white rounded disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                
                <div class="flex space-x-2">
                  <button 
                    v-for="(page, index) in documentPages" 
                    :key="index"
                    @click="currentPage = index"
                    :class="[
                      'px-3 py-1 rounded text-sm',
                      currentPage === index 
                        ? 'bg-blue-600 text-white' 
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    ]"
                  >
                    {{ index + 1 }}
                  </button>
                </div>
                
                <button 
                  @click="nextPage" 
                  :disabled="currentPage === documentPages.length - 1"
                  class="px-3 py-1 bg-blue-600 text-white rounded disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </div>
              
              <!-- Current Page Content -->
              <div class="bg-gray-50 p-6 rounded-md">
                <div v-if="documentPages.length > 1" class="flex justify-between items-center mb-4 pb-2 border-b border-gray-300">
                  <h4 class="font-medium text-gray-800">Page {{ currentPage + 1 }}</h4>
                  <span class="text-xs text-gray-500">{{ documentPages.length }} pages</span>
                </div>
                
                <div class="bg-white p-4 rounded border">
                  <pre class="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed">{{ getCurrentPageContent() }}</pre>
                </div>
              </div>
              
              <!-- Page Summary (if multiple pages) -->
              <div v-if="documentPages.length > 1" class="mt-4 bg-blue-50 p-4 rounded-md">
                <h4 class="font-medium text-blue-900 mb-2">Document Overview</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  <div 
                    v-for="(page, index) in documentPages" 
                    :key="index"
                    @click="currentPage = index"
                    class="bg-white p-3 rounded border cursor-pointer hover:border-blue-300 transition-colors"
                    :class="currentPage === index ? 'border-blue-500 bg-blue-50' : 'border-gray-200'"
                  >
                    <div class="font-medium text-sm text-gray-800 mb-1">Page {{ index + 1 }}</div>
                    <div class="text-xs text-gray-600 line-clamp-3">
                      {{ truncateText(page.content, 100) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Analysis Detail Modal with Categorized Issues and Recommendations -->
    <div v-if="selectedAnalysis" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="closeAnalysisModal">
      <div class="bg-white rounded-lg max-w-6xl w-full max-h-[90vh] overflow-hidden" @click.stop>
        <div class="flex justify-between items-center p-6 border-b">
          <h2 class="text-xl font-semibold">Analysis Results</h2>
          <button @click="closeAnalysisModal" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        <div class="p-6 overflow-y-auto max-h-[70vh]">
          <div v-if="selectedAnalysis && selectedAnalysis.length > 0" class="space-y-6">
            <div v-for="(result, index) in selectedAnalysis" :key="index" class="border rounded-lg p-4">
              <div class="flex justify-between items-start mb-4">
                <h3 class="font-medium text-gray-900">Analysis {{ index + 1 }}</h3>
                <span class="text-xs text-gray-500">{{ formatDate(result.created_at) }}</span>
              </div>
              
              <div v-if="result.content" class="space-y-6">
                <!-- Parse and display categorized analysis -->
                <div v-if="parseCategorizedAnalysis(result.content)" class="space-y-6">
                  <div v-for="(category, categoryIndex) in parseCategorizedAnalysis(result.content)" :key="categoryIndex" class="bg-gray-50 p-4 rounded-lg">
                    <!-- Category Header -->
                    <div class="mb-4">
                      <h4 class="text-xl font-bold text-gray-800 mb-2">{{ category.name }}</h4>
                      <div class="w-full h-px bg-gray-300"></div>
                    </div>
                    
                    <!-- Issues Section -->
                    <div v-if="category.issue" class="mb-4">
                      <div class="flex items-center mb-2">
                        <svg class="w-5 h-5 text-red-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                        </svg>
                        <h5 class="text-lg font-semibold text-red-800">Issue Identified</h5>
                      </div>
                      <div class="bg-red-50 border-l-4 border-red-400 p-4 rounded-r-md">
                        <div class="flex items-start">
                          <div class="flex-shrink-0">
                            <svg class="w-4 h-4 text-red-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                            </svg>
                          </div>
                          <div class="ml-3">
                            <p class="text-red-700 text-sm">{{ category.issue }}</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Recommendations Section -->
                    <div v-if="category.recommendation" class="mb-2">
                      <div class="flex items-center mb-2">
                        <svg class="w-5 h-5 text-green-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                        </svg>
                        <h5 class="text-lg font-semibold text-green-800">Recommendation</h5>
                      </div>
                      <div class="bg-green-50 border-l-4 border-green-400 p-4 rounded-r-md">
                        <div class="flex items-start">
                          <div class="flex-shrink-0">
                            <svg class="w-4 h-4 text-green-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                          </div>
                          <div class="ml-3">
                            <p class="text-green-700 text-sm">{{ category.recommendation }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Fallback for non-structured content -->
                <div v-else class="bg-gray-50 p-4 rounded text-sm">
                  <h4 class="text-sm font-medium text-gray-700 mb-2">Analysis Results:</h4>
                  <div v-if="isJsonString(result.content)" class="space-y-2">
                    <div v-for="(item, idx) in parseAnalysisContent(result.content)" :key="idx" class="bg-white p-3 rounded border-l-4 border-blue-500">
                      <div class="font-medium text-gray-800 mb-1">{{ getAnalysisCategory(item) }}</div>
                      <div class="text-gray-600 text-sm">{{ getAnalysisDescription(item) }}</div>
                    </div>
                  </div>
                  <div v-else>
                    <pre class="whitespace-pre-wrap">{{ result.content }}</pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else>
            <p class="text-gray-500">No analysis results available</p>
          </div>
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
      selectedAnalysis: null,
      analyzingDocs: [], // Track which documents are being analyzed
      batchAnalyzing: false,
      pollingIntervals: new Map(), // Track polling intervals for each document
      batchProgress: {
        show: false,
        total: 0,
        completed: 0,
        percentage: 0,
        startTime: null,
        estimatedTimeRemaining: null,
        recentlyCompleted: []
      },
      // Pagination data
      currentPage: 0,
      documentPages: []
    }
  },
  async mounted() {
    await this.loadHistory()
    await this.loadSummary()
  },
  beforeUnmount() {
    // Clear all polling intervals when component is destroyed
    this.pollingIntervals.forEach(interval => clearInterval(interval))
    this.pollingIntervals.clear()
  },
  methods: {
    async loadHistory() {
      this.loading = true
      this.error = null
      
      try {
        const response = await historyService.getUserHistory()

        // Access the data property from axios response
        this.documents = response.data?.documents || []
      } catch (error) {
        console.error('Error loading history:', error)
        this.error = error.response?.data?.error || 'Failed to load document history'
      } finally {
        this.loading = false
      }
    },
    
    async loadSummary() {
      try {
        const response = await historyService.getHistorySummary()
        this.summary = response.data || response
      } catch (error) {
        console.error('Error loading summary:', error)
      }
    },
    
    async refreshData() {
      // Refresh both history and summary data
      await Promise.all([
        this.loadHistory(),
        this.loadSummary()
      ])
    },
    
    // Process raw analysis results from backend
    processAnalysisResults(rawResults) {
      if (!rawResults || !Array.isArray(rawResults)) return []
      
      return rawResults.map(item => {
        // Extract content from the nested structure
        let content = ''
        
        if (item.result && item.result.choices && item.result.choices.length > 0) {
          content = item.result.choices[0].message?.content || ''
        }
        
        return {
          id: item.id,
          file_id: item.file_id,
          created_at: item.created_at,
          content: content
        }
      })
    },

    // Parse categorized analysis with proper structure: [Title], [Issue], [Recommendation] repeating
    parseCategorizedAnalysis(content) {
      if (!content) return null
      
      try {
        let parsedContent = content
        
        // If it's a JSON string, parse it first
        if (this.isJsonString(content)) {
          parsedContent = JSON.parse(content)
        }
        
        // Extract all bracket contents using regex
        const bracketMatches = parsedContent.match(/\[([^\]]+)\]/g)
        if (!bracketMatches || bracketMatches.length === 0) {
          return null
        }
        
        // Extract content from brackets (remove the [ ] characters)
        const bracketContents = bracketMatches.map(match => match.slice(1, -1).trim())
        
        const categories = []
        
        // Process items in groups of 3: Title, Issue, Recommendation
        for (let i = 0; i < bracketContents.length; i += 3) {
          const title = bracketContents[i]
          const issue = bracketContents[i + 1]
          const recommendation = bracketContents[i + 2]
          
          if (title) {
            categories.push({
              name: title,
              issue: issue || null,
              recommendation: recommendation || null
            })
          }
        }
        
        return categories.length > 0 ? categories : null
      } catch (e) {
        console.error('Error parsing categorized analysis:', e)
        return null
      }
    },
    
    // Parse document pages from text with page separators
    parseDocumentPages(text) {
      if (!text) return []
      
      // Split by page markers using regex
      const pageRegex = /--- Page \d+ ---/g
      const pages = text.split(pageRegex)
      
      // Remove empty pages and trim whitespace
      const cleanPages = pages
        .map(page => page.trim())
        .filter(page => page.length > 0)
        .map((page, index) => ({
          number: index + 1,
          content: page
        }))
      
      return cleanPages
    },
    
    // Format page content for better readability
    formatPageContent(content) {
      // Clean up extra whitespace and format paragraphs
      return content
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)
        .join('\n\n')
    },
    
    // Get current page content with formatting
    getCurrentPageContent() {
      if (this.documentPages.length === 0) return ''
      if (this.currentPage >= this.documentPages.length) return ''
      
      return this.formatPageContent(this.documentPages[this.currentPage].content)
    },
    
    // Navigation methods
    nextPage() {
      if (this.currentPage < this.documentPages.length - 1) {
        this.currentPage++
      }
    },
    
    previousPage() {
      if (this.currentPage > 0) {
        this.currentPage--
      }
    },
    
    initializeBatchProgress(totalDocuments) {
      this.batchProgress = {
        show: true,
        total: totalDocuments,
        completed: 0,
        percentage: 0,
        startTime: Date.now(),
        estimatedTimeRemaining: null,
        recentlyCompleted: []
      }
    },
    
    updateBatchProgress(newCompletedCount, completedDocument = null) {
      this.batchProgress.completed = newCompletedCount
      this.batchProgress.percentage = (newCompletedCount / this.batchProgress.total) * 100
      
      // Add to recently completed if document provided
      if (completedDocument) {
        this.batchProgress.recentlyCompleted.push(completedDocument)
        // Keep only last 10 completed documents
        if (this.batchProgress.recentlyCompleted.length > 10) {
          this.batchProgress.recentlyCompleted.shift()
        }
      }
      
      // Calculate estimated time remaining
      if (this.batchProgress.completed > 0 && this.batchProgress.completed < this.batchProgress.total) {
        const elapsed = Date.now() - this.batchProgress.startTime
        const avgTimePerDoc = elapsed / this.batchProgress.completed
        const remaining = this.batchProgress.total - this.batchProgress.completed
        const estimatedMs = remaining * avgTimePerDoc
        
        this.batchProgress.estimatedTimeRemaining = this.formatTimeRemaining(estimatedMs)
      }
    },
    
    formatTimeRemaining(ms) {
      const seconds = Math.floor(ms / 1000)
      const minutes = Math.floor(seconds / 60)
      const hours = Math.floor(minutes / 60)
      
      if (hours > 0) {
        return `${hours}h ${minutes % 60}m`
      } else if (minutes > 0) {
        return `${minutes}m ${seconds % 60}s`
      } else {
        return `${seconds}s`
      }
    },
    
    completeBatchProgress() {
      this.batchProgress.percentage = 100
      this.batchProgress.completed = this.batchProgress.total
      this.batchProgress.estimatedTimeRemaining = null
      
      // Hide progress bar after a delay and refresh page
      setTimeout(() => {
        this.batchProgress.show = false
        this.batchAnalyzing = false
        
        // Show completion message
        this.$toast?.success('All documents analyzed successfully! Refreshing data...')
        
        // Refresh the entire page data
        setTimeout(() => {
          this.refreshData()
        }, 1000)
      }, 2000)
    },
    
    async analyzeDocument(documentId) {
      if (this.analyzingDocs.includes(documentId)) return
      
      this.analyzingDocs.push(documentId)
      
      try {
        const response = await historyService.analyzeDocument(documentId)
        
        if (response.status === 202) {
          // Analysis started, show success message
          this.$toast?.success('Analysis started for document')
          
          // Start polling for this specific document
          this.startPollingForDocument(documentId)
        }
      } catch (error) {
        console.error('Error analyzing document:', error)
        this.error = error.response?.data?.error || 'Failed to start analysis'
        
        // Remove from analyzing list on error
        const index = this.analyzingDocs.indexOf(documentId)
        if (index > -1) {
          this.analyzingDocs.splice(index, 1)
        }
      }
    },
    
    async triggerBatchAnalysis() {
      if (this.batchAnalyzing) return
      
      this.batchAnalyzing = true
      
      try {
        const response = await historyService.analyzeBatchDocuments()
        
        if (response.status === 202) {
          const unanalyzedCount = response.data.unanalyzed_count
          
          // Initialize progress tracking
          this.initializeBatchProgress(unanalyzedCount)
          
          this.$toast?.success(`Batch analysis started for ${unanalyzedCount} documents`)
          
          // Start polling for batch analysis completion
          this.startBatchPolling()
        }
      } catch (error) {
        console.error('Error starting batch analysis:', error)
        this.error = error.response?.data?.error || 'Failed to start batch analysis'
        this.batchAnalyzing = false
        this.batchProgress.show = false
      }
    },
    
    startPollingForDocument(documentId) {
      // Clear existing interval if any
      if (this.pollingIntervals.has(documentId)) {
        clearInterval(this.pollingIntervals.get(documentId))
      }
      
      let pollCount = 0
      const maxPolls = 24 // Poll for max 2 minutes (24 * 5 seconds)
      
      const interval = setInterval(async () => {
        pollCount++
        
        try {
          const response = await historyService.getDocumentHistory(documentId)
          
          if (response.data.has_analysis) {
            // Analysis completed, refresh data and stop polling
            await this.refreshData()
            
            // Remove from analyzing list
            const index = this.analyzingDocs.indexOf(documentId)
            if (index > -1) {
              this.analyzingDocs.splice(index, 1)
            }
            
            // Clear interval
            clearInterval(interval)
            this.pollingIntervals.delete(documentId)
            
            this.$toast?.success('Document analysis completed!')
          } else if (pollCount >= maxPolls) {
            // Max polling reached, stop polling but keep in analyzing state
            clearInterval(interval)
            this.pollingIntervals.delete(documentId)
            
            // Remove from analyzing list after timeout
            const index = this.analyzingDocs.indexOf(documentId)
            if (index > -1) {
              this.analyzingDocs.splice(index, 1)
            }
            
            this.$toast?.info('Analysis is taking longer than expected. Please refresh manually.')
          }
        } catch (error) {
          console.error('Error polling document status:', error)
          
          // On error, stop polling and remove from analyzing list
          clearInterval(interval)
          this.pollingIntervals.delete(documentId)
          
          const index = this.analyzingDocs.indexOf(documentId)
          if (index > -1) {
            this.analyzingDocs.splice(index, 1)
          }
        }
      }, 5000) // Poll every 5 seconds
      
      this.pollingIntervals.set(documentId, interval)
    },
    
    startBatchPolling() {
      let pollCount = 0
      const maxPolls = 120 // Poll for max 10 minutes for batch operations
      const initialAnalyzedCount = this.summary?.documents_with_analysis || 0
      
      const interval = setInterval(async () => {
        pollCount++
        
        try {
          // Check summary to see if analysis completion rate has changed
          const summaryResponse = await historyService.getHistorySummary()
          const newSummary = summaryResponse.data || summaryResponse
          
          const currentAnalyzedCount = newSummary.documents_with_analysis
          const completedInBatch = currentAnalyzedCount - initialAnalyzedCount
          
          // Update progress
          this.updateBatchProgress(completedInBatch)
          
          // Check if batch is complete
          if (newSummary.documents_without_analysis === 0 || completedInBatch >= this.batchProgress.total) {
            clearInterval(interval)
            this.completeBatchProgress()
          } else if (pollCount >= maxPolls) {
            // Max polling reached
            clearInterval(interval)
            this.batchAnalyzing = false
            this.batchProgress.show = false
            
            // Refresh data one final time
            await this.refreshData()
            
            this.$toast?.info('Batch analysis is taking longer than expected. Data has been refreshed.')
          }
        } catch (error) {
          console.error('Error polling batch status:', error)
          
          // On error, stop batch analyzing and refresh data
          clearInterval(interval)
          this.batchAnalyzing = false
          this.batchProgress.show = false
          await this.refreshData()
        }
      }, 3000) // Poll every 3 seconds for more responsive progress updates
    },
    
    async checkAnalysisStatus(documentId) {
      try {
        const response = await historyService.getDocumentHistory(documentId)
        if (response.data.has_analysis) {
          // Analysis completed, refresh the list
          await this.refreshData()
        }
      } catch (error) {
        console.error('Error checking analysis status:', error)
      }
    },
    
    viewDocument(item) {
      this.selectedDocument = item.document
      this.currentPage = 0
      
      // Parse document pages when viewing
      const fileInfo = this.getFileInfo(item.document.file)
      if (fileInfo && fileInfo.text) {
        this.documentPages = this.parseDocumentPages(fileInfo.text)
      } else {
        this.documentPages = []
      }
    },
    
    viewAnalysis(item) {
      // Process the raw analysis results before setting selectedAnalysis
      this.selectedAnalysis = this.processAnalysisResults(item.analysis_results)
    },
    
    closeModal() {
      this.selectedDocument = null
      this.currentPage = 0
      this.documentPages = []
    },
    
    closeAnalysisModal() {
      this.selectedAnalysis = null
    },
    
    getFileInfo(file) {
      if (!file) return null
      
      // If file is a string, try to parse it as JSON
      if (typeof file === 'string') {
        try {
          const parsed = JSON.parse(file)
          return { text: parsed.text || '' }
        } catch (e) {
          return { text: file }
        }
      }
      
      // If file is already an object, extract only text
      return { text: file.text || '' }
    },
    
    isJsonString(str) {
      if (!str || typeof str !== 'string') return false
      try {
        const parsed = JSON.parse(str)
        return typeof parsed === 'string' && parsed.includes('[')
      } catch (e) {
        return false
      }
    },
    
    parseAnalysisContent(content) {
      if (!content) return []
      
      try {
        // If it's a JSON string containing analysis results
        if (this.isJsonString(content)) {
          const parsed = JSON.parse(content)
          // Split by semicolon and filter out empty items
          return parsed.split(';').filter(item => item.trim().length > 0)
        }
        
        // If it contains analysis patterns, split by common delimiters
        if (content.includes('[') && content.includes(']')) {
          return content.split(';').filter(item => item.trim().length > 0)
        }
        
        return [content]
      } catch (e) {
        return [content]
      }
    },
    
    getAnalysisCategory(item) {
      if (!item) return 'Analysis Item'
      
      // Extract category from patterns like [CATEGORY - SUBCATEGORY]
      const match = item.match(/\[([^\]]+)\]/)
      if (match) {
        return match[1].split(' - ')[0] || 'Analysis'
      }
      
      // For items without brackets, try to extract first few words as category
      const words = item.split(' ')
      if (words.length > 2) {
        return words.slice(0, 2).join(' ').toUpperCase()
      }
      
      return 'Analysis Item'
    },
    
    getAnalysisDescription(item) {
      if (!item) return ''
      
      // Remove the category part and get the description
      const parts = item.split('], ')
      if (parts.length > 1) {
        return parts.slice(1).join('], ').trim()
      }
      
      return item.trim()
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Unknown date'
      try {
        return new Date(dateString).toLocaleString()
      } catch (error) {
        return 'Invalid date'
      }
    },
    
    truncateText(text, maxLength) {
      if (!text) return ''
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }
  }
}
</script>

<style scoped>
/* Custom scrollbar for modals */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Progress bar animations */
.bg-blue-600 {
  transition: width 0.5s ease-out;
}

/* Line clamp utility for text truncation */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
