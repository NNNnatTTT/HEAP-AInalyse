import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: () => import('../views/LandingPage.vue')
    },
    {
      path: '/login',
      component: () => import('../views/LogInView.vue')
    },
    {
      path: '/signup',
      component: () => import('../views/SignUpView.vue')
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/compare',
      name: 'compare',
      component: () => import('../views/CompareView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/:notFound(.*)',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('jwt_token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/signup') && token) {
    next('/home')
  } else {
    next()
  }
})

export default router
