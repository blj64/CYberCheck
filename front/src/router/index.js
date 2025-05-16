import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/pages/Dashboard.vue'
import WebsiteDetails from '@/pages/WebsiteDetails.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/website/:id', name: 'WebsiteDetails', component: WebsiteDetails }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
