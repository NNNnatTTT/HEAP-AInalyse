<template>
  <nav class="bg-white shadow-md px-6 py-4 flex justify-between items-center">
    <div class="text-xl font-bold text-gray-800">AInalyse</div>
    
    <!-- Show navigation links only when user is logged in -->
    <div v-if="isLoggedIn" class="flex items-center space-x-6">
      <ul class="flex space-x-6">
        <li><router-link to="/home" class="text-gray-700 hover:text-blue-600">Home</router-link></li>
        <li><router-link to="/compare" class="text-gray-700 hover:text-blue-600">Compare</router-link></li>
        <li><router-link to="/about" class="text-gray-700 hover:text-blue-600">About</router-link></li>
      </ul>
      
      <!-- User info and logout -->
      <div class="flex items-center space-x-4 border-l border-gray-200 pl-6">
        <span v-if="userEmail" class="text-sm text-gray-600">{{ userEmail }}</span>
        <button
          @click="handleLogout"
          :disabled="loggingOut"
          class="text-gray-700 hover:text-red-600 transition-colors disabled:opacity-50"
        >
          {{ loggingOut ? 'Logging out...' : 'Logout' }}
        </button>
      </div>
    </div>
    
    <!-- Show login/signup links when user is not logged in -->
    <div v-else class="flex space-x-4">
      <router-link 
        to="/login" 
        class="text-gray-700 hover:text-blue-600 transition-colors"
      >
        Sign In
      </router-link>
      <router-link 
        to="/signup" 
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors"
      >
        Sign Up
      </router-link>
    </div>
  </nav>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '@/services'

const router = useRouter()
const loggingOut = ref(false)

// Reactive state for authentication
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('jwt_token')
})

const userEmail = computed(() => {
  const userInfo = localStorage.getItem('user_info')
  if (userInfo) {
    try {
      const user = JSON.parse(userInfo)
      return user.email
    } catch (error) {
      console.error('Error parsing user info:', error)
      return null
    }
  }
  return null
})

// Logout function
const handleLogout = async () => {
  loggingOut.value = true
  
  try {
    // Call auth service logout (clears local storage)
    await authService.logout()
    
    // Redirect to landing page
    router.push('/')
    
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    loggingOut.value = false
  }
}

// Optional: Verify token on component mount
onMounted(async () => {
  const token = localStorage.getItem('jwt_token')
  if (token) {
    try {
      // Verify token is still valid
      await authService.verify()
    } catch (error) {
      console.error('Token verification failed:', error)
      // Clear invalid token
      localStorage.removeItem('jwt_token')
      localStorage.removeItem('user_info')
    }
  }
})
</script>

.container {
  max-width: 100%;
  overflow-x: hidden;
}
