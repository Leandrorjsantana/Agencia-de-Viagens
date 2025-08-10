import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue' // Garante que estamos importando o arquivo correto

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // Futuramente, adicionaremos as outras rotas (login, registro, etc.) aqui.
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router