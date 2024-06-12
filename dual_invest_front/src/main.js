import './assets/main.css'

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'



const app = createApp(App).use(router)
app.provide("API_HOST", import.meta.env.VITE_API_HOST || 'ws://localhost:8000');
app.mount('#app')

