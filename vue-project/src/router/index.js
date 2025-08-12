import { createRouter, createWebHistory } from 'vue-router'
import SobreNosotros from '@/views/SobreNosotros.vue'


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
      
    }
  ],
})

export default router
