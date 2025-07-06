
// Authentication service
import api from './api'

// Authentication service - updated to match Flask auth service
export const authService = {
  register: (userData) => api.post('/auth/signup', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  verify: () => api.get('/auth/verify'),
  logout: () => {
    // Client-side logout - remove tokens
    localStorage.removeItem('jwt_token')
    localStorage.removeItem('user_info')
    return Promise.resolve({ message: 'Logged out successfully' })
  }
}


// Upload service
export const uploadService = {
  uploadContract: (formData) => api.post('/upload-service', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// // Analysis service
// export const analysisService = {
//   analyzeContract: (contractId) => api.post('/analyse', { contractId }),
//   getAnalysisResult: (analysisId) => api.get(`/analyse/${analysisId}`)
// }

export const analysisService = {
  analyzeContract: (pages, promptKey, prompt) =>
    api.post('/analyse', { pages, promptKey, prompt })
}


// Review service
export const reviewService = {
  getReview: (contractId) => api.get(`/review/${contractId}`),
  createReview: (reviewData) => api.post('/review', reviewData)
}

// Scanner service
export const scannerService = {
  scanContract: (contractId) => api.post('/scanner', { contractId }),
  getScanResults: (scanId) => api.get(`/scanner/${scanId}`)
}

// Suggestion service
export const suggestionService = {
  getSuggestions: (contractId) => api.get(`/suggestions/${contractId}`),
  createSuggestion: (suggestionData) => api.post('/suggestions', suggestionData)
}

// Suggestion history service
export const suggestionHistoryService = {
  getHistory: () => api.get('/suggestion-history'),
  getHistoryById: (id) => api.get(`/suggestion-history/${id}`)
}
