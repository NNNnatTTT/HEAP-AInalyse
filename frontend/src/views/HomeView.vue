<template>
  <div class="min-h-screen bg-gradient-to-r from-blue-600 to-purple-600 py-8">
    <div class="max-w-6xl mx-auto px-4">
      <!-- Header Section -->
      <div class="text-center mb-12 text-white">
        <h1 class="text-5xl font-bold mb-4 drop-shadow-lg">
          Contract Analysis Tool
        </h1>
        <p class="text-xl opacity-90 max-w-2xl mx-auto leading-relaxed">
          Upload your PDF contract document to analyze for suspicious clauses and potential risks
        </p>
      </div>

      <!-- Upload Section -->
      <div class="mb-16">
        <div class="bg-white rounded-xl p-8 shadow-2xl max-w-2xl mx-auto">
          <div 
            class="border-3 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer transition-all duration-300 bg-gray-50 hover:border-indigo-500 hover:bg-indigo-50"
            :class="{ 'border-indigo-500 bg-indigo-50': isDragOver }"
            @drop="handleDrop" 
            @dragover.prevent="handleDragOver" 
            @dragleave="handleDragLeave"
            @click="triggerFileInput"
          >
            <input 
              ref="fileInput" 
              type="file" 
              accept=".pdf"
              @change="handleFileSelect"
              class="hidden"
            />
            <div v-if="!selectedFile" class="space-y-4">
              <div class="text-6xl mb-4">📄</div>
              <h3 class="text-xl font-semibold text-gray-700 mb-2">
                Drop your PDF contract here or click to browse
              </h3>
              <p class="text-gray-600 mb-2">
                Supported format: PDF only
              </p>
              <p class="text-sm text-gray-500">
                Maximum file size: 10MB
              </p>
            </div>
            <div v-else class="p-4">
              <div class="flex items-center gap-4 bg-gray-100 p-4 rounded-lg">
                <div class="text-3xl">📄</div>
                <div class="flex-1 text-left">
                  <h4 class="font-semibold text-gray-800 truncate">{{ selectedFile.name }}</h4>
                  <p class="text-sm text-gray-600">{{ formatFileSize(selectedFile.size) }}</p>
                </div>
                <button 
                  @click.stop="removeFile" 
                  class="bg-red-500 hover:bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold transition-colors"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>

          <!-- Upload Button -->
          <div v-if="selectedFile" class="mt-6 text-center">
            <button 
              @click="uploadFile" 
              :disabled="isUploading"
              class="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-70 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-lg text-lg transition-all duration-200 transform hover:scale-105 hover:shadow-lg"
            >
              <span v-if="!isUploading">Analyze Contract</span>
              <span v-else>Analyzing... {{ uploadProgress }}%</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Results + Suggest Section -->
      <div
        v-if="analysisResult"
        class="max-w-2xl mx-auto mt-8 p-4 bg-white rounded-xl shadow-2xl"
      >
        <h2 class="text-2xl font-bold mb-4 text-gray-800">
          Contract Summary
        </h2>
        <ul class="list-disc pl-5 space-y-2 text-gray-700">
          <li v-for="(clause, i) in analysisResult" :key="i">
            <strong>{{ clause.title }}:</strong> {{ clause.summary }}
          </li>
        </ul>

        <!-- Suggest Improvements -->
        <div class="mt-6 text-center">
          <button
            @click="getSuggestion"
            :disabled="isSuggesting || !analysisId"
            class="cursor-pointer bg-green-500 hover:bg-green-600
                  disabled:opacity-70 disabled:cursor-not-allowed
                  text-white font-bold py-2 px-6 rounded-lg"
          >
            <span v-if="!isSuggesting">Suggest Improvements</span>
            <span v-else>Suggesting…</span>
          </button>
        </div>

        <!-- Suggestions Output -->
        <div v-if="suggestions" class="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 class="text-xl font-semibold mb-2">AI Suggestions</h3>
          <div v-if="suggestions.choices && suggestions.choices[0]">
            <div class="prose max-w-none">
              <p class="whitespace-pre-wrap">{{ suggestions.choices[0].message.content }}</p>
            </div>
          </div>
          <div v-else-if="suggestions.items">
            <ul class="list-disc pl-5 space-y-1">
              <li v-for="(s, idx) in suggestions.items" :key="idx">
                {{ s }}
              </li>
            </ul>
          </div>
          <div v-else>
            <p class="text-gray-600">{{ suggestions }}</p>
          </div>
        </div>
      </div>

      <!-- Features Section -->
      <div class="bg-white rounded-xl p-8 shadow-2xl">
        <h2 class="text-3xl font-bold text-center mb-8 text-gray-800">
          What We Analyze
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="text-center p-6 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 hover:transform hover:scale-105">
            <div class="text-4xl mb-4">🔍</div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">Suspicious Clauses</h3>
            <p class="text-gray-600 leading-relaxed">
              Identify potentially harmful or unfair contract terms
            </p>
          </div>
          <div class="text-center p-6 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 hover:transform hover:scale-105">
            <div class="text-4xl mb-4">⚠️</div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">Risk Assessment</h3>
            <p class="text-gray-600 leading-relaxed">
              Evaluate financial and legal risks in the agreement
            </p>
          </div>
          <div class="text-center p-6 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 hover:transform hover:scale-105">
            <div class="text-4xl mb-4">📋</div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">Key Terms</h3>
            <p class="text-gray-600 leading-relaxed">
              Highlight important dates, amounts, and obligations
            </p>
          </div>
          <div class="text-center p-6 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200 hover:transform hover:scale-105">
            <div class="text-4xl mb-4">💡</div>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">Recommendations</h3>
            <p class="text-gray-600 leading-relaxed">
              Get suggestions for contract improvements
            </p>
          </div>
        </div>
      </div>

      <!-- Error/Success Messages -->
      <div v-if="errorMessage" class="max-w-2xl mx-auto mt-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-center font-semibold">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="max-w-2xl mx-auto mt-6 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg text-center font-semibold">
        {{ successMessage }}
      </div>
    </div>

    <!-- Analysis Output -->
    <div
      v-if="pages.length"
      class="max-w-4xl mx-auto mt-10 bg-white p-8 rounded-xl shadow-xl"
    >
      <h2 class="text-2xl font-bold mb-4 text-gray-800">OCR Result</h2>
      <div
        v-for="(page, idx) in pages"
        :key="idx"
        class="mb-6 border-l-4 border-indigo-500 pl-4"
      >
        <h3 class="font-semibold mb-2 text-indigo-600">Page {{ idx + 1 }}</h3>
        <pre class="whitespace-pre-wrap text-gray-700">{{ page }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import { uploadService, suggestionService } from '@/services'

export default {
  name: 'HomeView',
  data() {
    return {
      selectedFile: null,
      isDragOver: false,
      isUploading: false,
      uploadProgress: 0,
      errorMessage: null,
      successMessage: null,
      analysisResult: null,
      pages: [],
      analysisId: null,
      isSuggesting: false,
      suggestions: null,
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click()
    },

    handleFileSelect(event) {
      const file = event.target.files[0]
      this.validateAndSetFile(file)
    },
    
    handleDrop(event) {
      event.preventDefault()
      this.isDragOver = false
      const file = event.dataTransfer.files[0]
      this.validateAndSetFile(file)
    },

    handleDragOver(event) {
      event.preventDefault()
      this.isDragOver = true
    },

    handleDragLeave() {
      this.isDragOver = false
    },

    validateAndSetFile(file) {
      this.errorMessage = null
      this.successMessage = null
      this.analysisResult = null
      this.suggestions = null // Clear previous suggestions

      if (!file) return

      // Validate file type - PDF only
      if (file.type !== 'application/pdf') {
        this.errorMessage = 'Please upload a PDF file only'
        return
      }

      // Validate file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        this.errorMessage = 'File size must be less than 10MB'
        return
      }

      this.selectedFile = file
      this.successMessage = 'PDF file selected successfully'
    },

    removeFile() {
      this.selectedFile = null
      this.errorMessage = null
      this.successMessage = null
      this.analysisResult = null
      this.suggestions = null
      this.analysisId = null
      this.$refs.fileInput.value = ''
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
    },
    
    async uploadFile() {
      if (!this.selectedFile) return
      
      this.isUploading = true
      this.errorMessage = null
      this.uploadProgress = 0
      this.suggestions = null // Clear previous suggestions

      try {
        const formData = new FormData()
        formData.append('file', this.selectedFile)

        this.uploadProgress = 10
        const uploadResponse = await uploadService.uploadContract(formData)
        this.uploadProgress = 100
        
        const result = uploadResponse.data
        this.analysisId = result.analysis_result_id

        // Process the analysis result for display
        const raw = result.choices?.[0]?.message?.content || ''
        const stripped = raw.replace(/^"|"$/g, '')
        const entries = stripped
          .split(';')
          .map(s => s.trim())
          .filter(Boolean)

        this.analysisResult = entries.map(entry => {
          const m = entry.match(/\[(.*?)\]\s*,\s*\[(.*?)\]\s*,\s*\[(.*?)\]/)
          if (!m) return { title: entry, summary: entry }
          const [, title, problem, suggestion] = m
          return { 
            title, 
            summary: problem + ' → ' + suggestion
          }
        })

        this.successMessage = 'File processed successfully!'
      } catch (error) {
        console.error('Upload error:', error)
        this.errorMessage =
          error.response?.data?.message || 'Upload failed. Please try again.'
      } finally {
        this.isUploading = false
        this.uploadProgress = 0
      }
    },

    async getSuggestion() {
      if (!this.analysisId) {
        this.errorMessage = 'No analysis ID available. Please upload and analyze a contract first.'
        return
      }

      this.isSuggesting = true
      this.suggestions = null
      this.errorMessage = null

      try {
        const suggestionData = {
          prompt_key: 'review',
          prompt: 'Please suggest improvements for these contract clauses and provide actionable recommendations.'
        }

        const response = await suggestionService.getSuggestions(this.analysisId, suggestionData)
        this.suggestions = response.data
        
        // If no suggestions received, show a message
        if (!this.suggestions || (this.suggestions.choices && this.suggestions.choices.length === 0)) {
          this.errorMessage = 'No suggestions were generated. Please try again.'
        }
      } catch (error) {
        console.error('Suggestion error:', error)
        this.errorMessage = error.response?.data?.error || error.message || 'Failed to get suggestions. Please try again.'
      } finally {
        this.isSuggesting = false
      }
    },
  }
}
</script>
