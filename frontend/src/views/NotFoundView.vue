<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
    <div class="max-w-lg mx-auto text-center">
      <!-- 404 Number -->
      <div class="mb-8">
        <h1 class="text-9xl font-bold text-indigo-600 leading-none">404</h1>
        <div class="text-2xl font-medium text-gray-600 mt-2">Page Not Found</div>
      </div>

      <!-- Illustration -->
      <div class="mb-8 flex justify-center">
        <svg class="w-64 h-48 text-indigo-300" fill="currentColor" viewBox="0 0 404 392" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="837c3e70-6c3a-44e6-8854-cc48c737b659" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <rect x="0" y="0" width="4" height="4" class="text-indigo-200" fill="currentColor" />
            </pattern>
          </defs>
          <rect width="404" height="392" fill="url(#837c3e70-6c3a-44e6-8854-cc48c737b659)" />
        </svg>
      </div>

      <!-- Message -->
      <div class="mb-8">
        <h2 class="text-2xl font-semibold text-gray-800 mb-4">Oops! Page not found</h2>
        <p class="text-gray-600 leading-relaxed">
          The page you're looking for doesn't exist or has been moved. 
          Don't worry, it happens to the best of us.
        </p>
      </div>

      <!-- Actions -->
      <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
        <button 
          @click="goBack"
          class="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          Go Back
        </button>
        
        <button 
          @click="goHome"
          class="w-full sm:w-auto bg-white hover:bg-gray-50 text-gray-700 px-6 py-3 rounded-lg font-medium border border-gray-300 transition-colors duration-200 flex items-center justify-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          Go Home
        </button>
      </div>

      <!-- Help Links -->
      <!-- <div class="mt-12 pt-8 border-t border-gray-200">
        <p class="text-sm text-gray-500 mb-4">Need help? Try these links:</p>
        <div class="flex flex-wrap justify-center gap-4 text-sm">
          <a href="#" @click.prevent="goToContact" class="text-indigo-600 hover:text-indigo-700 transition-colors">
            Contact Support
          </a>
          <span class="text-gray-300">•</span>
          <a href="#" @click.prevent="goToHelp" class="text-indigo-600 hover:text-indigo-700 transition-colors">
            Help Center
          </a>
          <span class="text-gray-300">•</span>
          <a href="#" @click.prevent="goToSitemap" class="text-indigo-600 hover:text-indigo-700 transition-colors">
            Sitemap
          </a>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  methods: {
    goBack() {
      // Go back to previous page
      this.$router.go(-1)
    },
    
    goHome() {
      // Navigate to home page
      this.$router.push('/home')
    },
    
    goToContact() {
      // Navigate to contact page
      this.$router.push('/contact')
    },
    
    goToHelp() {
      // Navigate to help page
      this.$router.push('/help')
    },
    
    goToSitemap() {
      // Navigate to sitemap
      this.$router.push('/sitemap')
    }
  },
  
  mounted() {
    // Optional: Track 404 errors for analytics
    console.warn('404 Error: Page not found -', window.location.href)
    
    // You can add analytics tracking here
    // this.$gtag?.event('page_not_found', {
    //   page_location: window.location.href,
    //   page_title: '404 Not Found'
    // })
  }
}
</script>

<style scoped>
/* Add some subtle animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.max-w-lg {
  animation: fadeIn 0.6s ease-out;
}

/* Floating animation for the 404 number */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

h1 {
  animation: float 3s ease-in-out infinite;
}
</style>