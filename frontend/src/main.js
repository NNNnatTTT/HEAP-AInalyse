import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import api from './services/api'

const app = createApp(App)

// Make API service available globally
app.config.globalProperties.$api = api

app.use(router)
app.mount('#app')
