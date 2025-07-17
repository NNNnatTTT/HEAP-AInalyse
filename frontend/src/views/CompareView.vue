<template>
  <div class="min-w-screen min-h-screen mx-auto p-8 font-sans
           bg-gradient-to-r from-blue-600 to-purple-600">
    <!-- Page Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-white mb-2 drop-shadow-lg">
        Contract Comparison
      </h1>
      <p class="text-lg text-white">
        Upload two contracts to compare their contents side by side
      </p>
    </div>

    <div class="mb-12">
      <!-- Top‐level Error -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
        <div class="flex">
          <svg class="h-5 w-5 text-red-400 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1
                 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1
                 0 101.414 1.414L10 11.414l1.293 1.293a1 1
                 0 001.414-1.414L11.414 10l1.293-1.293a1 1
                 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <div class="ml-3">
            <p class="text-sm text-red-800">{{ error }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <!-- Contract A Uploader -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
          <h3 class="bg-slate-50 px-6 py-4 m-0 text-xl font-semibold
                   text-gray-700 border-b border-gray-200">
            Contract A
          </h3>
          <div class="p-8 border-2 border-dashed border-gray-300 rounded-lg m-4
                   cursor-pointer transition-all duration-300 min-h-52
                   flex items-center justify-center
                   hover:border-blue-500 hover:bg-slate-50" :class="{
                    'border-blue-500 bg-blue-50': dragOverA,
                    'border-green-500 bg-green-50': contractA
                  }" @drop="handleDrop($event, 'A')" @dragover.prevent="dragOverA = true" @dragleave="dragOverA = false"
            @click="$refs.fileInputA.click()">
            <div v-if="!contractA" class="text-center">
              <svg class="w-16 h-16 text-gray-400 mb-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0
                     1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0
                     0l-3 3m3-3v12" />
              </svg>
              <p class="text-lg text-gray-700 mb-2">
                Drop your contract here or click to browse
              </p>
              <p class="text-sm text-gray-500">
                PDF, DOC, DOCX files supported
              </p>
            </div>
            <div v-else class="flex items-center gap-4 w-full">
              <svg class="w-12 h-12 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2
                     0 01-2-2V5a2 2 0 012-2h5.586a1
                     1 0 01.707.293l5.414 5.414a1
                     1 0 01.293.707V19a2 2 0 01-2
                     2z" />
              </svg>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-gray-700 mb-1 break-words">
                  {{ contractA.name }}
                </p>
                <p class="text-gray-500 text-sm">
                  {{ formatFileSize(contractA.size) }}
                </p>
              </div>
              <button class="bg-red-500 hover:bg-red-600 text-white rounded-full
                       w-8 h-8 flex items-center justify-center
                       transition-colors flex-shrink-0" @click.stop="removeFile('A')" title="Remove file">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          <input ref="fileInputA" type="file" accept=".pdf,.doc,.docx" @change="handleFileSelect($event, 'A')"
            style="display: none" />
        </div>

        <!-- Contract B Uploader -->
        <div class="bg-white rounded-xl shadow-lg overflow-hidden">
          <h3 class="bg-slate-50 px-6 py-4 m-0 text-xl font-semibold
                   text-gray-700 border-b border-gray-200">
            Contract B
          </h3>
          <div class="p-8 border-2 border-dashed border-gray-300 rounded-lg m-4
                   cursor-pointer transition-all duration-300 min-h-52
                   flex items-center justify-center
                   hover:border-blue-500 hover:bg-slate-50" :class="{
                    'border-blue-500 bg-blue-50': dragOverB,
                    'border-green-500 bg-green-50': contractB
                  }" @drop="handleDrop($event, 'B')" @dragover.prevent="dragOverB = true" @dragleave="dragOverB = false"
            @click="$refs.fileInputB.click()">
            <div v-if="!contractB" class="text-center">
              <svg class="w-16 h-16 text-gray-400 mb-4 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5
                     0 1115.9 6L16 6a5 5 0 011 9.9M15
                     13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="text-lg text-gray-700 mb-2">
                Drop your contract here or click to browse
              </p>
              <p class="text-sm text-gray-500">
                PDF, DOC, DOCX files supported
              </p>
            </div>
            <div v-else class="flex items-center gap-4 w-full">
              <svg class="w-12 h-12 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2
                     2 0 01-2-2V5a2 2 0 012-2h5.586a1
                     1 0 01.707.293l5.414 5.414a1
                     1 0 01.293.707V19a2 2 0 01-2
                     2z" />
              </svg>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-gray-700 mb-1 break-words">
                  {{ contractB.name }}
                </p>
                <p class="text-gray-500 text-sm">
                  {{ formatFileSize(contractB.size) }}
                </p>
              </div>
              <button class="bg-red-500 hover:bg-red-600 text-white rounded-full
                       w-8 h-8 flex items-center justify-center
                       transition-colors flex-shrink-0" @click.stop="removeFile('B')" title="Remove file">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          <input ref="fileInputB" type="file" accept=".pdf,.doc,.docx" @change="handleFileSelect($event, 'B')"
            style="display: none" />
        </div>
      </div>

      <!-- Compare Button -->
      <div class="text-center">
        <button class="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white
                 px-8 py-4 rounded-lg text-lg font-semibold inline-flex
                 items-center gap-2 transition-all duration-200" :disabled="!contractA || !contractB || isComparing"
          @click="compareContracts">
          <svg v-if="isComparing" class="w-5 h-5 spinner" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 0 1 8-8V0C5.373
                 0 0 5.373 0 12h4zm2 5.291A7.962
                 7.962 0 0 1 4 12H0c0 3.042 1.135
                 5.824 3 7.938l3-2.647z" />
          </svg>
          <span v-if="isComparing">Comparing...</span>
          <span v-else>Compare Contracts</span>
        </button>
      </div>

      <!-- Comparison Results -->
      <div v-if="comparisonResults" class="bg-white rounded-xl p-8 shadow-lg mt-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-6">
          Contract Comparison Analysis
        </h2>
        <div class="mb-6 text-sm text-gray-600">
          Comparing: <span class="font-medium">{{ comparisonResults.contractA_filename || contractA?.name }}</span>
          vs <span class="font-medium">{{ comparisonResults.contractB_filename || contractB?.name }}</span>
        </div>

        <!-- Parsed Comparison Clauses -->
        <div v-if="parsedClauses.length" class="space-y-6">
          <div v-for="(clause, index) in parsedClauses" :key="index" class="border rounded-lg p-6 bg-gray-50">
            <h3 class="text-lg font-semibold mb-4 border-b pb-2">
              {{ clause.title }}
            </h3>
            <div class="grid md:grid-cols-2 gap-4">
              <!-- Left column: Contract A -->
              <div class="bg-blue-50 p-4 rounded border-l-4 border-blue-400">
                <h4 class="font-medium text-blue-800 mb-3">
                  {{ comparisonResults.contractA_filename || contractA?.name }}
                </h4>
                <p class="text-sm text-gray-700 leading-relaxed">
                  {{ clause.contractA }}
                </p>
              </div>

              <!-- Right column: Contract B -->
              <div class="bg-green-50 p-4 rounded border-l-4 border-green-400">
                <h4 class="font-medium text-green-800 mb-3">
                  {{ comparisonResults.contractB_filename || contractB?.name }}
                </h4>
                <p class="text-sm text-gray-700 leading-relaxed">
                  {{ clause.contractB }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Failure: Could not parse -->
        <div v-else class="bg-red-50 border border-red-200 p-6 rounded-md text-center">
          <p class="text-red-700 mb-4">
            We couldn't read the comparison response. Please click "Retry" to try again.
          </p>
          <button class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold"
            @click="retryComparison">
            Retry
          </button>
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
      if (!this.comparisonResults) return []

      // 1) grab the raw bracket‐delimited text
      let raw = ''
      if (typeof this.comparisonResults === 'string') {
        raw = this.comparisonResults
      }
      else if (this.comparisonResults.choices?.[0]?.message?.content) {
        raw = this.comparisonResults.choices[0].message.content
      }
      else if (this.comparisonResults.content) {
        raw = this.comparisonResults.content
      }
      else if (this.comparisonResults.response) {
        raw = this.comparisonResults.response
      }
      else {
        return []
      }

      // 2) extract all "[ … ]" segments
      const matches = raw.match(/\[([^\]]+)\]/g)
      if (!matches) return []

      // 3) strip brackets and trim
      const segments = matches.map(m => m.slice(1, -1).trim())

      // 4) every 3 segments → one clause object
      const clauses = []
      for (let i = 0; i < segments.length; i += 3) {
        const [title, contractA, contractB] = segments.slice(i, i + 3)
        if (title && contractA && contractB) {
          clauses.push({
            title,
            contractA: contractA.trim(),
            contractB: contractB.trim()
          })
        }
      }

      return clauses
    }
  },

  methods: {
    // Retry if parsing failed
    retryComparison() {
      this.comparisonResults = null
      this.compareContracts()
    },

    // Call the API and log raw data
    async compareContracts() {
      if (!this.contractA || !this.contractB) return

      this.isComparing = true
      this.error = null
      this.comparisonResults = null

      try {
        const fd = new FormData()
        fd.append('contractA', this.contractA)
        fd.append('contractB', this.contractB)

        const res = await compareService.compareContracts(fd)

        // // 🔍 Inspect exactly what the API returned
        // console.log('compareContracts → raw response data:', res.data)
        // console.log('Type of response data:', typeof res.data)

        this.comparisonResults = res.data
      } catch (e) {
        console.error('compareContracts → error:', e)
        this.error =
          e.response?.data?.error ||
          e.response?.data?.msg ||
          'Comparison failed. Please try again.'
      } finally {
        this.isComparing = false
      }
    },

    handleFileSelect(event, contract) {
      const file = event.target.files[0]
      if (file) this.validateAndSetFile(file, contract)
    },

    handleDrop(event, contract) {
      event.preventDefault()
      this[`dragOver${contract}`] = false
      const file = event.dataTransfer.files[0]
      if (file) this.validateAndSetFile(file, contract)
    },

    validateAndSetFile(file, contract) {
      const allowed = [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/msword'
      ]
      if (!allowed.includes(file.type)) {
        this.error = 'Please upload PDF, DOCX or DOC'
        return
      }
      if (file.size > 10 * 1024 * 1024) {
        this.error = 'File must be smaller than 10 MB'
        return
      }
      this[`contract${contract}`] = file
      this.error = null
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
      return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]
    }
  }
}
</script>

<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.spinner {
  animation: spin 1s linear infinite;
}
</style>
