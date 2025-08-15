import { createRouter, createWebHistory } from 'vue-router'

import SobreNosotros from '@/views/SobreNosotros.vue'

import Error404 from '@/views/Error404.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      component: ()=>import('@/views/home.vue'),
      name:'home'
    },
    {
      path:'/sobre-nosotros',
      component: SobreNosotros

    },
    {
      path:'/:pathMatch(.*)*',
      component: Error404
    }
  ],
})

export default router
