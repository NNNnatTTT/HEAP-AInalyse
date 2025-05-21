// SAMPLE
import axios from 'axios'

export function loginUser(credentials) {
  return axios.post('/api/login', credentials)
}

export function fetchUserData() {
  return axios.get('/api/user')
}
