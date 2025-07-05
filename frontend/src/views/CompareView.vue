<template>
  <div class="min-w-screen min-h-screen mx-auto p-8 font-sans bg-gradient-to-r from-blue-600 to-purple-600">
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-white mb-2 drop-shadow-lg">Contract Comparison</h1>
      <p class="text-lg text-white">Upload two contracts to compare their contents side by side</p>
    </div>

    <div class="mb-12">
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

    <!-- Comparison Results -->
    <div
      v-if="comparisonResults"
      class="bg-white rounded-xl p-8 shadow-lg"
    >
      <h2 class="text-2xl font-semibold text-gray-800 mb-6">
        Comparison Results
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Left column: Contract A -->
        <div>
          <h3 class="text-xl font-medium text-gray-700 mb-2">
            Contract A
          </h3>
          <div
            class="border rounded-lg p-4 h-64 overflow-auto whitespace-pre-wrap bg-gray-50"
          >
            {{ getContractA() }}
          </div>
        </div>

        <!-- Right column: Contract B -->
        <div>
          <h3 class="text-xl font-medium text-gray-700 mb-2">
            Contract B
          </h3>
          <div
            class="border rounded-lg p-4 h-64 overflow-auto whitespace-pre-wrap bg-gray-50"
          >
            {{ getContractB() }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { scanDocument } from '@/api/scanner';                // ← scanner first
import { sendComparePrompt } from '@/api/compact-compare-api'; // ← then your compare/prompt API

export default {
  name: 'CompareView',
  data() {
    return {
      contractA: null,
      contractB: null,
      isComparing: false,
      comparisonResults: null
    };
  },
  methods: {
    // … your drag/drop handlers untouched …

    async compareContracts() {
      if (!this.contractA || !this.contractB) return;
      this.isComparing = true;
      this.comparisonResults = null;

      try {
        const form = new FormData();
        form.append('fileA', this.contractA);
        form.append('fileB', this.contractB);

        const resp = await fetch('http://localhost:3000/api/compare', {
          method: 'POST',
          body: form
        });
        if (!resp.ok) throw new Error(await resp.text());
        this.comparisonResults = await resp.json();
      } catch (err) {
        alert('Comparison failed: ' + err.message);
      } finally {
        this.isComparing = false;
      }
    }

  }
};
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
