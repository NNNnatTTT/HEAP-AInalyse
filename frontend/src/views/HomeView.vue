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

          <!-- Upload Button with Loading Spinner -->
          <div v-if="selectedFile" class="mt-6 text-center">
            <button 
              @click="uploadFile" 
              :disabled="isUploading"
              class="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-70 disabled:cursor-not-allowed text-white font-bold py-3 px-8 rounded-lg text-lg transition-all duration-200 transform hover:scale-105 hover:shadow-lg"
            >
              <template v-if="!isUploading">
                Analyze Contract
              </template>
              <template v-else>
                <span class="flex items-center justify-center">
                  Analyzing
                  &nbsp;
                  <svg class="animate-spin mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
              </template>
            </button>
          </div>


        </div>
      </div>

      <!-- Results Section -->
      <div v-if="analysisResult" class="max-w-2xl mx-auto mt-8 p-6 bg-gradient-to-br from-gray-100 to-white rounded-xl shadow-xl border border-gray-200">
        <h2 class="text-2xl font-bold mb-6 text-gray-900 text-center rounded-t-lg p-4 border-b border-gray-300">Contract Overview</h2>
        <div class="space-y-5">
          <div v-for="(clause, i) in analysisResult" :key="i" class="bg-white rounded-lg shadow-lg p-5 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <h3 class="text-xl font-semibold text-gray-800 mb-3 bg-blue-50 p-2 rounded" style="text-transform: none;">{{ clause.title }}</h3>
            <p class="text-gray-600 leading-relaxed">
              <span class="font-medium text-gray-800">Issue:</span> {{ clause.issue }}
              <br><br>
              <span class="font-medium text-gray-800">Suggestion:</span> {{ clause.suggestion }}
            </p>
          </div>
        </div>
      </div>

      <!-- Features Section -->
      <section v-if="!analysisResult || !analysisResult.length" class="mt-6 p-4 bg-blue-50 rounded shadow">
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
      </section>

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
import { uploadService} from '@/services'

export default {
  name: 'HomeView',
  data() {
    return {
      selectedFile: null,
      isDragOver: false,
      isUploading: false,
      errorMessage: null,
      successMessage: null,
      analysisResult: null,
      pages: []
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
      this.$refs.fileInput.value = ''
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`
    },

    parseSummary(summary) {
      const [issue, suggestion] = summary.split(' -> ');
      return {
        issue: issue.trim(),
        suggestion: suggestion ? suggestion.trim() : ''
      };
    }, 

    async uploadFile() {
      if (!this.selectedFile) return
      
      this.isUploading = true
      this.errorMessage = null

      try {
        const formData = new FormData()
        formData.append('file', this.selectedFile)

        const uploadResponse = await uploadService.uploadContract(formData)

        const result = uploadResponse.data
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
          const { issue, suggestion: parsedSuggestion } = this.parseSummary(`${problem} -> ${suggestion}`);
          return { 
            title, 
            issue,
            suggestion: parsedSuggestion
          }
        })
        this.successMessage = 'File processed successfully!'
      } catch (error) {
        console.error('Upload error:', error)
        this.errorMessage =
          error.response?.data?.message || 'Upload failed. Please try again.'
      } finally {
        this.isUploading = false
      }
    }
  }
}
</script>