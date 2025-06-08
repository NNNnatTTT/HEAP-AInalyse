<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 py-12">
    <div class="max-w-7xl mx-auto px-4">
      <!-- Hero Section -->
      <div class="text-center mb-16">
        <h1 class="text-5xl font-bold text-gray-900 mb-6">
          Protecting Workers Through Contract Awareness
        </h1>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
          Most workers sign contracts without fully understanding what they're agreeing to. 
          Our AI-powered tool helps you identify potential risks and unfair terms before you sign, 
          ensuring you make informed decisions about your employment future.
        </p>
      </div>

      <!-- Worker-Focused Statistics Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
        <div class="bg-white rounded-xl p-6 shadow-lg text-center border-l-4 border-red-500">
          <div class="text-3xl font-bold text-red-600 mb-2">78%</div>
          <p class="text-gray-600">Of workers don't fully understand their employment contracts</p>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-lg text-center border-l-4 border-orange-500">
          <div class="text-3xl font-bold text-orange-600 mb-2">1 in 4</div>
          <p class="text-gray-600">Workers have experienced contract-related disputes</p>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-lg text-center border-l-4 border-blue-500">
          <div class="text-3xl font-bold text-blue-600 mb-2">$3,200</div>
          <p class="text-gray-600">Average cost workers pay for legal advice on contracts</p>
        </div>
        <div class="bg-white rounded-xl p-6 shadow-lg text-center border-l-4 border-green-500">
          <div class="text-3xl font-bold text-green-600 mb-2">85%</div>
          <p class="text-gray-600">Of contract issues could be prevented with proper review</p>
        </div>
      </div>

      <!-- Contract Issues Chart - Fixed sizing -->
      <div class="bg-white rounded-xl p-8 shadow-lg mb-16">
        <h2 class="text-3xl font-bold text-gray-900 mb-6 text-center">
          Most Common Contract Issues Workers Face
        </h2>
        <div class="chart-container">
          <canvas ref="issuesChart"></canvas>
        </div>
        <p class="text-center text-gray-600 mt-4">
          These are the top contract issues that affect workers, many of which can be identified before signing
        </p>
      </div>

      <!-- Two Column Charts - Fixed sizing -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
        <div class="bg-white rounded-xl p-8 shadow-lg">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Why Workers Don't Review Contracts</h3>
          <div class="chart-container-small">
            <canvas ref="reasonsChart"></canvas>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-8 shadow-lg">
          <h3 class="text-2xl font-bold text-gray-900 mb-6">Contract Review Benefits</h3>
          <div class="chart-container-small">
            <canvas ref="benefitsChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Our Mission Section -->
      <div class="bg-white rounded-xl p-12 shadow-lg mb-16">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-4xl font-bold text-gray-900 mb-8">Empowering Workers, One Contract at a Time</h2>
          <p class="text-lg text-gray-700 leading-relaxed mb-8">
            We believe every worker deserves to understand what they're signing. Legal jargon shouldn't 
            prevent you from protecting your rights and interests. Our AI breaks down complex contract 
            language into plain English, highlighting potential red flags and unfair terms that could 
            impact your career and financial well-being.
          </p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
            <div class="text-center">
              <div class="bg-red-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl">⚠️</span>
              </div>
              <h4 class="text-xl font-semibold mb-2">Spot Red Flags</h4>
              <p class="text-gray-600">Identify unfair clauses, excessive penalties, and suspicious terms before you sign</p>
            </div>
            <div class="text-center">
              <div class="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl">📖</span>
              </div>
              <h4 class="text-xl font-semibold mb-2">Plain English Explanations</h4>
              <p class="text-gray-600">Transform legal jargon into clear, understandable language</p>
            </div>
            <div class="text-center">
              <div class="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl">💪</span>
              </div>
              <h4 class="text-xl font-semibold mb-2">Know Your Rights</h4>
              <p class="text-gray-600">Understand your protections and what you can negotiate</p>
            </div>
          </div>
        </div>
      </div>

      <!-- What We Help You Identify -->
      <div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-12 text-white mb-16">
        <h2 class="text-4xl font-bold text-center mb-12">What We Help You Identify</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="text-center">
            <h4 class="text-xl font-semibold mb-3">Non-Compete Clauses</h4>
            <p class="opacity-90">Understand restrictions on future employment and their enforceability</p>
          </div>
          <div class="text-center">
            <h4 class="text-xl font-semibold mb-3">Termination Terms</h4>
            <p class="opacity-90">Know your rights regarding notice periods, severance, and wrongful dismissal</p>
          </div>
          <div class="text-center">
            <h4 class="text-xl font-semibold mb-3">Overtime & Benefits</h4>
            <p class="opacity-90">Verify fair compensation structures and benefit entitlements</p>
          </div>
          <div class="text-center">
            <h4 class="text-xl font-semibold mb-3">Intellectual Property</h4>
            <p class="opacity-90">Understand what work belongs to you vs. your employer</p>
          </div>
          <div class="text-center">
            <h4 class="text-xl font-semibold mb-3">Confidentiality Limits</h4>
            <p class="opacity-90">Ensure NDAs don't prevent you from reporting illegal activities</p>
          </div>
          <div class="text-center">
            <h4 class="text-xl font-semibold mb-3">Dispute Resolution</h4>
            <p class="opacity-90">Know your options if conflicts arise with your employer</p>
          </div>
        </div>
      </div>

      <!-- Call to Action -->
      <div class="text-center bg-white rounded-xl p-12 shadow-lg">
        <h2 class="text-3xl font-bold text-gray-900 mb-4">
          Don't Sign Blind - Review Smart
        </h2>
        <p class="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
          Upload your contract today and get instant insights into potential risks, 
          unfair terms, and areas you should negotiate. It's free, confidential, and takes just minutes.
        </p>
        <router-link 
          to="/" 
          class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-lg text-lg transition-all duration-200 transform hover:scale-105 inline-block"
        >
          Analyze Your Contract Now
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'

export default {
  name: 'AboutView',
  data() {
    return {
      issuesChart: null,
      reasonsChart: null,
      benefitsChart: null
    }
  },
  mounted() {
    // Use nextTick to ensure DOM is fully rendered
    this.$nextTick(() => {
      this.createIssuesChart()
      this.createReasonsChart()
      this.createBenefitsChart()
    })
  },
  beforeUnmount() {
    // Properly destroy charts to prevent memory leaks
    if (this.issuesChart) {
      this.issuesChart.destroy()
      this.issuesChart = null
    }
    if (this.reasonsChart) {
      this.reasonsChart.destroy()
      this.reasonsChart = null
    }
    if (this.benefitsChart) {
      this.benefitsChart.destroy()
      this.benefitsChart = null
    }
  },
  methods: {
    createIssuesChart() {
      const ctx = this.$refs.issuesChart?.getContext('2d')
      if (!ctx) return
      
      this.issuesChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Unclear Termination', 'Excessive Non-Compete', 'Unpaid Overtime', 'Vague Job Duties', 'No Severance', 'Unfair Penalties'],
          datasets: [{
            label: 'Percentage of Workers Affected',
            data: [45, 38, 42, 35, 40, 28],
            backgroundColor: 'rgba(239, 68, 68, 0.8)',
            borderColor: 'rgb(239, 68, 68)',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              max: 50,
              title: {
                display: true,
                text: 'Percentage of Workers (%)'
              }
            }
          }
        }
      })
    },
    
    createReasonsChart() {
      const ctx = this.$refs.reasonsChart?.getContext('2d')
      if (!ctx) return
      
      this.reasonsChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Too Complex', 'Time Pressure', 'Trust Employer', 'Cost of Legal Help', 'Don\'t Know How'],
          datasets: [{
            data: [32, 28, 18, 15, 7],
            backgroundColor: [
              'rgba(239, 68, 68, 0.8)',
              'rgba(245, 158, 11, 0.8)',
              'rgba(59, 130, 246, 0.8)',
              'rgba(16, 185, 129, 0.8)',
              'rgba(139, 92, 246, 0.8)'
            ],
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                boxWidth: 12,
                font: {
                  size: 11
                }
              }
            }
          }
        }
      })
    },
    
    createBenefitsChart() {
      const ctx = this.$refs.benefitsChart?.getContext('2d')
      if (!ctx) return
      
      this.benefitsChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Avoided Bad Terms', 'Better Negotiation', 'Peace of Mind', 'Saved Money'],
          datasets: [{
            label: 'Benefit Reported (%)',
            data: [72, 68, 85, 45],
            backgroundColor: 'rgba(16, 185, 129, 0.8)',
            borderColor: 'rgb(16, 185, 129)',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: 'y',
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            x: {
              beginAtZero: true,
              max: 100,
              title: {
                display: true,
                text: 'Percentage (%)'
              }
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}

.chart-container-small {
  position: relative;
  height: 300px;
  width: 100%;
}

/* Prevent chart overflow */
.chart-container canvas,
.chart-container-small canvas {
  max-width: 100% !important;
  height: auto !important;
}
</style>
