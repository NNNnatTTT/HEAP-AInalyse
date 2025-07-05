<template>
  <div class="min-h-screen flex flex-col bg-white">
    <section class="bg-gradient-to-br from-blue-50 via-white to-purple-50 flex-grow px-12 py-24">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div class="space-y-8">
            <div class="space-y-4">
              <h1 class="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Analyze Contracts with
                <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AI Precision
                </span>
              </h1>
              <p class="text-xl text-gray-600 leading-relaxed max-w-2xl">
                Transform your contract review process with AI-powered analysis. Compare, identify risks, and extract key terms in minutes, not hours.
              </p>
            </div>
            
            <div class="flex flex-col sm:flex-row gap-4">
              <button @click="startAnalyzing" class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
                Start Analyzing Now
              </button>
            </div>
          </div>
          
          <div class="relative">
            <div class="bg-white rounded-2xl shadow-2xl p-8 transform rotate-1 hover:rotate-0 transition-transform duration-300">
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <h3 class="font-semibold text-gray-800">Contract Analysis</h3>
                  <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                </div>
                <div class="space-y-3">
                  <div class="h-4 bg-gradient-to-r from-blue-200 to-blue-100 rounded-full"></div>
                  <div class="h-4 bg-gradient-to-r from-purple-200 to-purple-100 rounded-full w-4/5"></div>
                  <div class="h-4 bg-gradient-to-r from-green-200 to-green-100 rounded-full w-3/5"></div>
                </div>
                <div class="pt-4 border-t border-gray-100">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-600">Risk Score</span>
                    <span class="font-semibold text-green-600">Low Risk</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Floating elements -->
            <div class="absolute -top-4 -right-4 w-20 h-20 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full opacity-20 animate-bounce"></div>
            <div class="absolute -bottom-8 -left-4 w-16 h-16 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full opacity-20 animate-pulse"></div>
          </div>
        </div>
      </div>
    </section>
    <!-- Footer -->
   <!-- Footer -->
    <footer class="bg-gray-900 text-gray-400 py-6">
        <div class="text-center text-sm">
            &copy; 2025 AInalyse. All rights reserved.
        </div>
    </footer>

  </div>
</template>

<script>
export default {
  name: 'LandingPageView',
  data() {
    return {
      features: [
        {
          title: 'AI-Powered Analysis',
          description: 'Advanced machine learning algorithms analyze contract language, identify potential risks, and highlight important clauses automatically.',
          icon: 'AiIcon'
        },
        {
          title: 'Contract Comparison',
          description: 'Compare multiple contracts side-by-side to identify differences, inconsistencies, and negotiation opportunities.',
          icon: 'CompareIcon'
        },
        {
          title: 'Risk Assessment',
          description: 'Get comprehensive risk scores and detailed explanations of potential legal and financial risks in your contracts.',
          icon: 'RiskIcon'
        },
        {
          title: 'Key Term Extraction',
          description: 'Automatically extract and categorize important terms, dates, obligations, and financial information.',
          icon: 'ExtractIcon'
        },
        {
          title: 'Compliance Checking',
          description: 'Verify contract compliance with industry standards, regulations, and your organization\'s policies.',
          icon: 'ComplianceIcon'
        },
        {
          title: 'Export & Integration',
          description: 'Export analysis results and integrate with your existing legal management systems and workflows.',
          icon: 'IntegrationIcon'
        }
      ],
      steps: [
        {
          title: 'Upload Your Contract',
          description: 'Simply drag and drop your contract files (PDF, DOC, DOCX) or upload them through our secure interface.'
        },
        {
          title: 'AI Analysis',
          description: 'Our advanced AI engine analyzes your contract, identifying key terms, risks, and important clauses within minutes.'
        },
        {
          title: 'Review Results',
          description: 'Get comprehensive analysis reports with risk assessments, recommendations, and actionable insights.'
        }
      ]
    }
  },
  methods: {
    startAnalyzing() {
      // Navigate to contract analysis page
      this.$router.push('/login')
    },
  },
  components: {
    // Icon components for features
    AiIcon: {
      template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/></svg>`
    },
    CompareIcon: {
      template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"/></svg>`
    },
    RiskIcon: {
      template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>`
    },
    ExtractIcon: {
      template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>`
    },
    ComplianceIcon: {
      template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>`
    },
    IntegrationIcon: {
      template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0"/></svg>`
    }
  }
}
</script>

<style scoped>
/* Smooth scrolling for anchor links */
html {
  scroll-behavior: smooth;
}

/* Custom animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0.8,0,1,1);
  }
  50% {
    transform: none;
    animation-timing-function: cubic-bezier(0,0,0.2,1);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-bounce {
  animation: bounce 1s infinite;
}

/* Gradient text support for older browsers */
.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}
</style>