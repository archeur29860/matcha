import { createRouter, createWebHistory } from 'vue-router'
import TestPageChedo from '../vues/testPageChedo.vue'
import TestPageMinotte from '../vues/testPageMinotte.vue'

import DemoTestInteraction from '@/vues/demos/demoTestInteraction.vue'
import DemoTestBlocked from '@/vues/demos/demoTestBlocked.vue'
import AppLayout from '@/components/appLayout.vue'
import HomePage from '@/vues/HomePage.vue'

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
    {
      path: '/demo',
      children: [
        {
          path: 'interaction',
          name: 'interaction-demo',
          component: DemoTestInteraction,
        },
        {
          path: 'blocked',
          name: 'blocked-demo',
          component: DemoTestBlocked,
        },
      ],
    },
    {
      path: '',
      name: 'layout-navigation',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'redirect-home-page',
          redirect: '/home',
        },
        {
          path: 'home',
          name: 'home-page',
          component: HomePage
        },
      ]
    },
  ],
})

export default router
