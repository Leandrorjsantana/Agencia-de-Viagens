import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

// Vamos criar um componente genérico para as páginas que ainda não existem
const PlaceholderPage = { template: '<div class="container" style="padding: 50px 20px;"><h2>Página em Construção</h2></div>' };

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  // CORREÇÃO: Adicionando as rotas que faltavam para os links do menu
  { path: '/login', name: 'login', component: PlaceholderPage },
  { path: '/experiencias', name: 'experiencias', component: PlaceholderPage },
  { path: '/destinos', name: 'destinos', component: PlaceholderPage },
  { path: '/serviços', name: 'serviços', component: PlaceholderPage },
  { path: '/blog', name: 'blog', component: PlaceholderPage },
  { path: '/contato', name: 'contato', component: PlaceholderPage },
  { path: '/quemsomos', name: 'quemsomos', component: PlaceholderPage },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router