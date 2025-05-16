// services/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000', // ou `http://web:8000` si tu es dans Docker
})

export const getWebsites = () => api.get('/websites')
export const addWebsite = (data) => api.post('/websites', data)
