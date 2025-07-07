<template>
  <div class="min-w-screen min-h-screen mx-auto p-8 font-sans bg-gradient-to-r from-blue-600 to-purple-600">
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-white mb-2 drop-shadow-lg">Contract Comparison</h1>
      <p class="text-lg text-white">Upload two contracts to compare their contents side by side</p>
    </div>

    <div class="mb-12">
      <!-- Error Message Display -->
<div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
  <div class="flex">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
      </svg>
    </div>
    <div class="ml-3">
      <p class="text-sm text-red-800">{{ error }}</p>
    </div>
  </div>
</div>
  
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <!-- First Contract Uploader -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
          <h3 class="bg-slate-50 px-6 py-4 m-0 text-xl font-semibold text-gray-700 border-b border-gray-200">Contract A</h3>
          <div 
            class="p-8 border-2 border-dashed border-gray-300 rounded-lg m-4 cursor-pointer transition-all duration-300 min-h-52 flex items-center justify-center hover:border-blue-500 hover:bg-slate-50"
            :class="{ 
              'border-blue-500 bg-blue-50': dragOverA, 
              'border-green-500 bg-green-50': contractA 
            }"
            @drop="handleDrop($event, 'A')"
            @dragover.prevent="dragOverA = true"
            @dragleave="dragOverA = false"
            @click="$refs.fileInputA.click()"
          >
            <div v-if="!contractA" class="text-center">
              <svg class="w-16 h-16 text-gray-400 mb-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
              </svg>
              <p class="text-lg text-gray-700 mb-2">Drop your contract here or click to browse</p>
              <p class="text-sm text-gray-500">PDF, DOC, DOCX files supported</p>
            </div>
            <div v-else class="flex items-center gap-4 w-full">
              <svg class="w-12 h-12 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-gray-700 mb-1 break-words">{{ contractA.name }}</p>
                <p class="text-gray-500 text-sm">{{ formatFileSize(contractA.size) }}</p>
              </div>
              <button 
                class="bg-red-500 hover:bg-red-600 text-white border-none rounded-full w-8 h-8 flex items-center justify-center cursor-pointer transition-colors flex-shrink-0"
                @click.stop="removeFile('A')"
                title="Remove file"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>
          <input 
            ref="fileInputA"
            type="file" 
            accept=".pdf,.doc,.docx"
            @change="handleFileSelect($event, 'A')"
            style="display: none"
          />
        </div>

        <!-- Second Contract Uploader -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
          <h3 class="bg-slate-50 px-6 py-4 m-0 text-xl font-semibold text-gray-700 border-b border-gray-200">Contract B</h3>
          <div 
            class="p-8 border-2 border-dashed border-gray-300 rounded-lg m-4 cursor-pointer transition-all duration-300 min-h-52 flex items-center justify-center hover:border-blue-500 hover:bg-slate-50"
            :class="{ 
              'border-blue-500 bg-blue-50': dragOverB, 
              'border-green-500 bg-green-50': contractB 
            }"
            @drop="handleDrop($event, 'B')"
            @dragover.prevent="dragOverB = true"
            @dragleave="dragOverB = false"
            @click="$refs.fileInputB.click()"
          >
            <div v-if="!contractB" class="text-center">
              <svg class="w-16 h-16 text-gray-400 mb-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
              </svg>
              <p class="text-lg text-gray-700 mb-2">Drop your contract here or click to browse</p>
              <p class="text-sm text-gray-500">PDF, DOC, DOCX files supported</p>
            </div>
            <div v-else class="flex items-center gap-4 w-full">
              <svg class="w-12 h-12 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-gray-700 mb-1 break-words">{{ contractB.name }}</p>
                <p class="text-gray-500 text-sm">{{ formatFileSize(contractB.size) }}</p>
              </div>
              <button 
                class="bg-red-500 hover:bg-red-600 text-white border-none rounded-full w-8 h-8 flex items-center justify-center cursor-pointer transition-colors flex-shrink-0"
                @click.stop="removeFile('B')"
                title="Remove file"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>
          </div>
          <input 
            ref="fileInputB"
            type="file" 
            accept=".pdf,.doc,.docx"
            @change="handleFileSelect($event, 'B')"
            style="display: none"
          />
        </div>
      </div>

      <!-- Compare Button -->
      <div class="text-center">
        <button 
          class="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white border-none px-8 py-4 rounded-lg text-lg font-semibold cursor-pointer transition-all duration-200 inline-flex items-center gap-2 hover:transform hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:transform-none"
          :disabled="!contractA || !contractB || isComparing"
          @click="compareContracts"
        >
          <svg v-if="isComparing" class="w-5 h-5 spinner" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span v-if="isComparing">Comparing...</span>
          <span v-else>Compare Contracts</span>
        </button>
      </div>
    </div>

<!-- Updated Comparison Results Display -->
<div v-if="comparisonResults" class="bg-white rounded-xl p-8 shadow-lg">
  <h2 class="text-2xl font-semibold text-gray-800 mb-6">
    Contract Comparison Analysis
  </h2>
  
  <div class="mb-4 text-sm text-gray-600">
    Comparing: <span class="font-medium">{{ comparisonResults.contractA_filename || contractA?.name }}</span> 
    vs <span class="font-medium">{{ comparisonResults.contractB_filename || contractB?.name }}</span>
  </div>
  
  <!-- Debug Information (remove after fixing) -->
  <div class="mb-4 p-4 bg-yellow-50 border border-yellow-200 rounded">
    <h4 class="font-medium text-yellow-800 mb-2">Debug Info:</h4>
    <pre class="text-xs text-yellow-700">{{ JSON.stringify(comparisonResults, null, 2) }}</pre>
  </div>
  
  <!-- Parsed Comparison Clauses -->
  <div v-if="parsedClauses.length > 0" class="space-y-6">
    <div v-for="(clause, index) in parsedClauses" :key="index" 
         class="border rounded-lg p-6 bg-gray-50">
      <h3 class="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
        {{ clause.title }}
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-blue-50 p-4 rounded border-l-4 border-blue-400">
          <h4 class="font-medium text-blue-800 mb-2">Contract A</h4>
          <p class="text-sm text-gray-700 leading-relaxed">{{ clause.contractA }}</p>
        </div>
        <div class="bg-green-50 p-4 rounded border-l-4 border-green-400">
          <h4 class="font-medium text-green-800 mb-2">Contract B</h4>
          <p class="text-sm text-gray-700 leading-relaxed">{{ clause.contractB }}</p>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Fallback Raw Display -->
  <div v-else class="space-y-4">
    <h3 class="text-lg font-semibold text-gray-800">Raw Comparison Result:</h3>
    <div class="bg-gray-50 p-4 rounded border">
      <pre class="whitespace-pre-wrap text-sm">{{ getDisplayContent() }}</pre>
    </div>
  </div>
</div>


  </div>
</template>

<script>
import { compareService } from '@/services'

export default {
  name: 'CompareView',
  data() {
    return {
      contractA: null,
      contractB: null,
      dragOverA: false,
      dragOverB: false,
      isComparing: false,
      comparisonResults: null,
      error: null
    }
  },
  computed: {
  parsedClauses() {
    // Handle different response structures
    let content = null
    
    // Check for choices format (OpenAI-style response)
    if (this.comparisonResults?.choices?.[0]?.message?.content) {
      content = this.comparisonResults.choices[0].message.content
    }
    // Check for direct content
    else if (this.comparisonResults?.content) {
      content = this.comparisonResults.content
    }
    // Check for response field
    else if (this.comparisonResults?.response) {
      content = this.comparisonResults.response
    }
    // Check if the entire result is a string
    else if (typeof this.comparisonResults === 'string') {
      content = this.comparisonResults
    }
    
    if (!content) return []
    
    try {
      // Remove outer quotes if present
      const cleanContent = content.replace(/^'|'$/g, '')
      
      const clauses = cleanContent.split(';').map(clause => {
        const parts = clause.trim().match(/\[([^\]]+)\]/g)
        if (parts && parts.length === 3) {
          return {
            title: parts[0].slice(1, -1),
            contractA: parts[1].slice(1, -1),
            contractB: parts[2].slice(1, -1)
          }
        }
        return null
      }).filter(Boolean)
      
      return clauses
    } catch (error) {
      console.error('Error parsing comparison results:', error)
      return []
    }
  }
}

,
  methods: {
    handleFileSelect(event, contract) {
      const file = event.target.files[0]
      if (file) {
        this.validateAndSetFile(file, contract)
      }
    },

    handleDrop(event, contract) {
      event.preventDefault()
      this[`dragOver${contract}`] = false
      
      const file = event.dataTransfer.files[0]
      if (file) {
        this.validateAndSetFile(file, contract)
      }
    },

    validateAndSetFile(file, contract) {
      // Validate file type
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']
      if (!allowedTypes.includes(file.type)) {
        this.error = 'Please upload a valid document format (PDF, DOCX, DOC)'
        return
      }

      // Validate file size (10MB limit)
      if (file.size > 10 * 1024 * 1024) {
        this.error = 'File size must be less than 10MB'
        return
      }

      this[`contract${contract}`] = file
      this.error = null
      
      // Log file info for debugging
      console.log(`Contract ${contract} selected:`, {
        name: file.name,
        size: file.size,
        type: file.type
      })
    },

    removeFile(contract) {
      this[`contract${contract}`] = null
      this.comparisonResults = null
      this.error = null
    },

    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },

    async compareContracts() {
      if (!this.contractA || !this.contractB) return
      
      this.isComparing = true
      this.comparisonResults = null
      this.error = null

      // Debug logging
      console.log('Starting comparison with files:', {
        contractA: { name: this.contractA.name, size: this.contractA.size },
        contractB: { name: this.contractB.name, size: this.contractB.size }
      })

      try {
        // Create FormData with both contracts
        const formData = new FormData()
        formData.append('contractA', this.contractA)
        formData.append('contractB', this.contractB)

        // Debug FormData contents
        console.log('FormData entries:')
        for (let [key, value] of formData.entries()) {
          console.log(key, value instanceof File ? `File: ${value.name}` : value)
        }

        // Call compare service through Kong gateway
        const comparisonResponse = await compareService.compareContracts(formData)
        console.log('Raw comparison response:', comparisonResponse.data)
        
        this.comparisonResults = comparisonResponse.data

        // Parse the comparison results if they're in the specified format
        this.parseComparisonResults()

      } catch (error) {
        console.error('Comparison error:', error)
        console.error('Error response:', error.response?.data)
        this.error = error.response?.data?.error || error.response?.data?.msg || 'Comparison failed. Please try again.'
      } finally {
        this.isComparing = false
      }
    },

    parseComparisonResults() {
      // Check if the result is a string in the specified format from your prompt
      if (this.comparisonResults && typeof this.comparisonResults === 'string') {
        try {
          console.log('Parsing string result:', this.comparisonResults)
          
          // Parse the formatted string into structured data
          const clauses = this.comparisonResults.split(';').map(clause => {
            const parts = clause.trim().match(/\[([^\]]+)\]/g)
            if (parts && parts.length === 3) {
              return {
                title: parts[0].slice(1, -1),
                contractA: parts[1].slice(1, -1),
                contractB: parts[2].slice(1, -1)
              }
            }
            return null
          }).filter(Boolean)

          if (clauses.length > 0) {
            console.log('Parsed clauses:', clauses)
            this.comparisonResults = { 
              clauses,
              contractA_filename: this.contractA.name,
              contractB_filename: this.contractB.name
            }
          }
        } catch (error) {
          console.error('Error parsing comparison results:', error)
        }
      } else if (this.comparisonResults && typeof this.comparisonResults === 'object') {
        // Handle object response format
        console.log('Object result received:', this.comparisonResults)
        
        // Add filenames to the response if not already present
        if (!this.comparisonResults.contractA_filename) {
          this.comparisonResults.contractA_filename = this.contractA.name
        }
        if (!this.comparisonResults.contractB_filename) {
          this.comparisonResults.contractB_filename = this.contractB.name
        }
      }
    },

    getContractA() {
      if (this.comparisonResults?.clauses) {
        return this.comparisonResults.clauses
          .map(clause => `${clause.title}:\n${clause.contractA}`)
          .join('\n\n')
      }
      
      // Handle different response formats
      return this.comparisonResults?.contractA?.content || 
             this.comparisonResults?.analysis?.contractA || 
             this.comparisonResults?.text_a ||
             this.comparisonResults?.response ||
             'Contract A analysis will appear here after comparison'
    },

    getContractB() {
      if (this.comparisonResults?.clauses) {
        return this.comparisonResults.clauses
          .map(clause => `${clause.title}:\n${clause.contractB}`)
          .join('\n\n')
      }
      
      // Handle different response formats
      return this.comparisonResults?.contractB?.content || 
             this.comparisonResults?.analysis?.contractB || 
             this.comparisonResults?.text_b ||
             this.comparisonResults?.response ||
             'Contract B analysis will appear here after comparison'
    }
  }
}
</script>
<style scoped>
@keyframes spin {
  from { transform: rotate(0deg); }
  to   { transform: rotate(360deg); }
}
.spinner {
  animation: spin 1s linear infinite;
}
</style>
