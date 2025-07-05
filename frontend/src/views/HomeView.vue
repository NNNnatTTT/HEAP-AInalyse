<template>
  <div class="min-h-screen bg-gradient-to-r from-blue-600 to-purple-600 py-8">
    <div class="max-w-6xl mx-auto px-4">
      <!-- Header Section -->
      <div class="text-center mb-12 text-white">
        <h1 class="text-5xl font-bold mb-4 drop-shadow-lg">
          Contract Analysis Tool
        </h1>
        <p class="text-xl opacity-90 max-w-2xl mx-auto leading-relaxed">
          Upload your contract document to analyze for suspicious clauses and potential risks
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
              accept=".pdf,.docx,.doc,.jpg,.jpeg,.png,.gif"
              @change="handleFileSelect"
              class="hidden"
            />
            
            <div v-if="!selectedFile" class="space-y-4">
              <div class="text-6xl mb-4">📄</div>
              <h3 class="text-xl font-semibold text-gray-700 mb-2">
                Drop your contract here or click to browse
              </h3>
              <p class="text-gray-600 mb-2">
                Supported formats: PDF, DOCX, DOC, JPG, PNG, GIF
              </p>
              <p class="text-sm text-gray-500">
                Maximum file size: 10MB
              </p>
            </div>
            
            <div v-else class="p-4">
              <div class="flex items-center gap-4 bg-gray-100 p-4 rounded-lg">
                <div class="text-3xl">{{ getFileIcon(selectedFile.type) }}</div>
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
  </div>
</template>

<script>
import { uploadService, analysisService } from '@/services'

export default {
  name: 'HomeView',
  data() {
    return {
      selectedFile: null,
      uploading: false,
      error: null,
      analysisResult: null
    }
  },
  methods: {
    handleFileSelect(event) {
      this.selectedFile = event.target.files[0]
      this.error = null
      this.analysisResult = null
    },
    
    handleDrop(event) {
      event.preventDefault()
      this.selectedFile = event.dataTransfer.files[0]
      this.error = null
      this.analysisResult = null
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
    async uploadFile() {
      if (!this.selectedFile) return
      
      // Validate file size (10MB limit)
      if (this.selectedFile.size > 10 * 1024 * 1024) {
        this.error = 'File size must be less than 10MB'
        return
      }
      
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword', 'image/jpeg', 'image/png', 'image/gif']
      if (!allowedTypes.includes(this.selectedFile.type)) {
        this.error = 'Please upload a valid file format (PDF, DOCX, DOC, JPG, PNG, GIF)'
        return
      }
      
      this.uploading = true
      this.error = null
      
      try {
        const formData = new FormData()
        formData.append('file', this.selectedFile)
        
        // Upload file through Kong gateway
        const uploadResponse = await uploadService.uploadContract(formData)
        const contractId = uploadResponse.data.contractId
        
        // Trigger analysis
        const analysisResponse = await analysisService.analyzeContract(contractId)
        this.analysisResult = analysisResponse.data
        
        // Clear selected file after successful upload
        this.selectedFile = null
        
      } catch (error) {
        console.error('Upload/Analysis error:', error)
        this.error = error.response?.data?.message || 'Upload failed. Please try again.'
      } finally {
        this.uploading = false
      }
    }
  }
}
</script>
