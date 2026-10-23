import { createRouter, createWebHistory } from 'vue-router'
import TestPageChedo from '../vues/testPageChedo.vue'
import TestPageMinotte from '../vues/testPageMinotte.vue'

import DemoTestInteraction from '@/vues/demos/demoTestInteraction.vue'
import DemoTestBlocked from '@/vues/demos/demoTestBlocked.vue'
import AppLayout from '@/vues/navigation/appLayout.vue'
import HomePage from '@/vues/navigation/HomePage.vue'
import ProfileViewer from '@/vues/navigation/ProfileViewer.vue'
import InteractionHistory from '@/vues/InteractionHistory.vue'
import LoginPage from '@/vues/auth/LoginPage.vue'
import SocketTest from '@/components/SocketTest.vue';
import SignupPage from '@/vues/auth/SignupPage.vue'

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
        {
          path: '/socket-test',
          name: 'SocketTest',
          component: SocketTest,
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
        {
          path: 'profile/:user_id',
          name: 'my-profile',
          component: ProfileViewer
        },
        {
          path: 'interaction_history',
          name: 'interaction-history',
          component: InteractionHistory
        },
      ]
    },
    {
      path: '/login',
      name: 'login-page',
      component: LoginPage
    },
    {
      path: '/signup',
      name: 'signup-page',
      component: SignupPage
    }
  ],
})

export default router
