import { createRouter, createWebHistory } from 'vue-router'


const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('@/views/LandingPage.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/analysis',
    name: 'analysis',
    component: () => import('@/views/AnalysisView.vue')
  },
  {
    path: '/compare',
    name: 'compare',
    component: () => import('@/views/CompareView.vue')
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/AboutView.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'notFound',
    component: () => import('@/views/NotFoundView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
