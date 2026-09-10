import { createRouter, createWebHistory } from 'vue-router'
import TestPageChedo from '../vues/testPageChedo.vue'
import TestPageMinotte from '../vues/testPageMinotte.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  
  routes: [
    {
      path: '/test/chedo',
      name: 'testchedo',
      component: TestPageChedo,
    },
    {
      path: '/test/minotte',
      name: 'testminotte',
      component: TestPageMinotte,
    },
    
  ],
})

export default router
