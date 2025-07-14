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

// Upload service - corrected endpoint path
export const uploadService = {
  uploadContract: (formData) => api.post('/upload-service', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// Analysis service - using AI model endpoint
export const analysisService = {
  analyzeContract: (pages, promptKey, prompt) =>
    api.post('/analyse', { pages, promptKey, prompt }),
  compareContracts: (data) => api.post('/analyse/compare', data)
}

// Scanner service - matches Kong configuration
export const scannerService = {
  scanContract: (formData) => api.post('/scanner', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getScanResults: (scanId) => api.get(`/scanner/${scanId}`)
}

// Compare service - for contract comparison functionality
export const compareService = {
  compareContracts: (formData) => api.post('/compare/compare', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getComparisonResult: (comparisonId) => api.get(`/compare/${comparisonId}`)
}

export const historyService = {

  async getUserHistory() {
    const response = await api.get('/history')
    return response
  },
  
  async getHistorySummary() {
    const response = await api.get('/history/summary')
    return response
  },
  
  async getDocumentHistory(documentId) {
    const response = await api.get(`/history/${documentId}`)
    return response
  },
  
  async getDocumentAnalysis(documentId) {
    const response = await api.get(`/history/analysis/${documentId}`)
    return response
  },
  
  // ADD THESE NEW METHODS:
  async analyzeDocument(documentId) {
    const response = await api.post(`/history/analyze/${documentId}`)
    return response
  },
  
  async analyzeBatchDocuments() {
    const response = await api.post('/history/analyze-batch')
    return response
  }
}

// Commented out services that are not currently active in Kong
// Uncomment when these services are enabled

// // Review service
// export const reviewService = {
//   getReview: (contractId) => api.get(`/review/${contractId}`),
//   createReview: (reviewData) => api.post('/review', reviewData)
// }

// Suggestion service
export const suggestionService = {
  getSuggestions: (resultId, suggestionData) => api.post(`/suggestions/${resultId}`, suggestionData),
  createSuggestion: (suggestionData) => api.post('/suggestions', suggestionData)
}

// // Suggestion history service
// export const suggestionHistoryService = {
//   getHistory: () => api.get('/suggestion-history'),
//   getHistoryById: (id) => api.get(`/suggestion-history/${id}`)
// }

// // Open router wrapper service
// export const openRouterService = {
//   processRequest: (data) => api.post('/open-router', data)
// }
