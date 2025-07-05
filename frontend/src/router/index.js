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
  // routes: [
  //   {
  //     path: '/',
  //     component: () => import('../views/LandingPage.vue')
  //   },
  //   {
  //     path: '/login',
  //     component: () => import('../views/LogInView.vue')
  //   },
  //   {
  //     path: '/signup',
  //     component: () => import('../views/SignUpView.vue')
  //   },
  //   {
  //     path: '/home',
  //     name: 'home',
  //     component: () => import('../views/HomeView.vue'),
  //   },
  //   {
  //     path: '/about',
  //     name: 'about',
  //     // route level code-splitting
  //     // this generates a separate chunk (About.[hash].js) for this route
  //     // which is lazy-loaded when the route is visited.
  //     component: () => import('../views/AboutView.vue'),
  //   },
  //   {
  //     path: '/compare',
  //     name: 'compare',
  //     // route level code-splitting
  //     // this generates a separate chunk (About.[hash].js) for this route
  //     // which is lazy-loaded when the route is visited.
  //     component: () => import('../views/CompareView.vue'),
  //   },
  //   {
  //     path: '/:notFound(.*)',
  //     component: () => import('../views/NotFoundView.vue'),
  //   },
  // ],
  routes
})

export default router
