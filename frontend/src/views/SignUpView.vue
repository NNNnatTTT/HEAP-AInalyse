<template>
  <div
    class="min-h-screen bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-extrabold text-white drop-shadow-lg">
          Create your account
        </h2>
        <p class="mt-2 text-sm text-white/80">
          Already have an account?
          <router-link to="/login"
            class="text-white hover:text-white font-medium relative group transition-colors duration-200 ml-1">
            Sign in here
            <span
              class="absolute left-0 bottom-0 w-0 h-0.5 bg-gradient-to-r from-pink-400 to-yellow-400 transition-all duration-300 group-hover:w-full"></span>
          </router-link>
        </p>
      </div>

      <div class="bg-white shadow-xl rounded-lg p-8">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Success Message -->
          <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-md p-4 mb-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-green-800">{{ successMessage }}</p>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="error" class="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-red-800">{{ error }}</p>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="firstName" class="block text-sm font-medium text-gray-700 mb-2">
                First Name
              </label>
              <input id="firstName" v-model="form.firstName" type="text" required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors"
                placeholder="John" />
            </div>

            <div>
              <label for="lastName" class="block text-sm font-medium text-gray-700 mb-2">
                Last Name
              </label>
              <input id="lastName" v-model="form.lastName" type="text" required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors"
                placeholder="Doe" />
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email address
            </label>
            <input id="email" v-model="form.email" type="email" required
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors"
              placeholder="john@example.com" />
            <p v-if="emailError" class="mt-1 text-sm text-red-600">{{ emailError }}</p>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div class="relative">
              <input id="password" v-model="form.password" :type="showPassword ? 'text' : 'password'" required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors pr-10"
                placeholder="Create a password" />
              <button type="button" @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600">
                <svg v-if="showPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                </svg>
                <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>

            <!-- Password strength indicator -->
            <div class="mt-2">
              <div class="flex space-x-1">
                <div v-for="i in 4" :key="i" class="h-1 w-1/4 rounded-full transition-colors"
                  :class="passwordStrength >= i ? getStrengthColor(passwordStrength) : 'bg-gray-200'"></div>
              </div>
              <p class="mt-1 text-xs text-gray-600">
                Password must be at least 8 characters with uppercase, lowercase, and numbers
              </p>
            </div>
          </div>

          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirm Password
            </label>
            <div class="relative">
              <input id="confirmPassword" v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'" required
                class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-colors pr-10"
                placeholder="Confirm your password" />
              <button type="button" @click="showConfirmPassword = !showConfirmPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600">
                <svg v-if="showConfirmPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21" />
                </svg>
                <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
            <p v-if="passwordMismatch" class="mt-1 text-sm text-red-600">Passwords do not match</p>
          </div>

          <div class="flex items-center">
            <input id="terms" v-model="form.acceptTerms" type="checkbox" required
              class="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded" />
            <label for="terms" class="ml-2 block text-sm text-gray-900">
              I agree to the
              <a href="#" class="text-purple-600 hover:text-purple-500 font-medium">Terms of Service</a>
              and
              <a href="#" class="text-purple-600 hover:text-purple-500 font-medium">Privacy Policy</a>
            </label>
          </div>

          <div>
            <button type="submit" :disabled="loading || !isFormValid"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:bg-purple-400 disabled:cursor-not-allowed transition-colors">
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg"
                fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              {{ loading ? 'Creating account...' : 'Create account' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '@/services'

export default {
  name: 'SignUpView',
  data() {
    return {
      form: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        acceptTerms: false
      },
      showPassword: false,
      showConfirmPassword: false,
      loading: false,
      error: null,
      successMessage: null
    }
  },
  computed: {
    emailError() {
      if (!this.form.email) return null
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      return !emailRegex.test(this.form.email) ? 'Please enter a valid email address' : null
    },
    passwordMismatch() {
      return this.form.password !== this.form.confirmPassword && this.form.confirmPassword.length > 0
    },
    passwordStrength() {
      const password = this.form.password
      if (!password) return 0

      let strength = 0
      if (password.length >= 8) strength++
      if (/[a-z]/.test(password)) strength++
      if (/[A-Z]/.test(password)) strength++
      if (/[0-9]/.test(password)) strength++

      return strength
    },
    isFormValid() {
      return this.form.firstName &&
        this.form.lastName &&
        this.form.email &&
        this.form.password &&
        this.form.confirmPassword &&
        this.form.acceptTerms &&
        !this.emailError &&
        !this.passwordMismatch &&
        this.form.password.length >= 8
    }
  },
  methods: {
    getStrengthColor(strength) {
      switch (strength) {
        case 1: return 'bg-red-500'
        case 2: return 'bg-yellow-500'
        case 3: return 'bg-blue-500'
        case 4: return 'bg-green-500'
        default: return 'bg-gray-200'
      }
    },

    async handleSubmit() {
      if (!this.isFormValid) return

      this.loading = true
      this.error = null
      this.successMessage = null

      try {
        // Step 1: Register the user
        const signupResponse = await authService.register({
          Email: this.form.email,
          Password: this.form.password
        })

        // Show initial success message
        this.successMessage = 'Account created successfully! Logging you in...'

        // Step 2: Automatically log the user in
        try {
          const loginResponse = await authService.login({
            Email: this.form.email,
            Password: this.form.password
          })

          // Store JWT token and user info
          // In your login component's handleSubmit method
          localStorage.setItem('jwt_token', response.data.access_token)
          if (response.data.user) {
            localStorage.setItem('user_info', JSON.stringify(response.data.user))
          }

          // Trigger navbar update
          if (window.refreshAuth) {
            window.refreshAuth()
          }


          // Update success message
          this.successMessage = 'Welcome! Redirecting to your dashboard...'

          // Clear the form
          this.form = {
            firstName: '',
            lastName: '',
            email: '',
            password: '',
            confirmPassword: '',
            acceptTerms: false
          }

          // Redirect to home page after a short delay
          setTimeout(() => {
            this.$router.push('/home')
          }, 1500)

        } catch (loginError) {
          console.error('Auto-login failed:', loginError)
          // If auto-login fails, redirect to login page
          this.successMessage = 'Account created! Please sign in to continue.'
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        }

      } catch (signupError) {
        console.error('Registration error:', signupError)
        this.error = signupError.response?.data?.msg || 'Registration failed. Please try again.'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
