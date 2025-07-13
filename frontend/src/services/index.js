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

// History service - for retrieving user document history and analysis results
export const historyService = {
  // Get all documents for the current user with their analysis results
  getUserHistory: () => api.get('/history'),
  
  // Get specific document with its analysis results
  getDocumentHistory: (documentId) => api.get(`/history/${documentId}`),
  
  // Get only the analysis results for a specific document
  getDocumentAnalysis: (documentId) => api.get(`/history/analysis/${documentId}`),
  
  // Get summary statistics of user's document history
  getHistorySummary: () => api.get('/history/summary')
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
