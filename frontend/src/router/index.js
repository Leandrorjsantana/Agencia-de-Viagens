import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'

// Componente genérico para páginas em construção
const PlaceholderPage = { template: '<div class="container" style="padding: 50px 20px;"><h2>Página em Construção</h2><p>O conteúdo para esta seção estará disponível em breve.</p></div>' };

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  
  // --- CORREÇÃO AQUI: Adicionando as rotas que faltavam ---
  { path: '/experiencias', name: 'experiencias', component: PlaceholderPage },
  { path: '/destinos', name: 'destinos', component: PlaceholderPage },
  { path: '/servicos', name: 'servicos', component: PlaceholderPage },
  { path: '/blog', name: 'blog', component: PlaceholderPage },
  { path: '/sobre-nos', name: 'sobre-nos', component: PlaceholderPage },
  { path: '/contato', name: 'contato', component: PlaceholderPage },
  { path: '/ajuda', name: 'ajuda', component: PlaceholderPage },
  { path: '/televendas', name: 'televendas', component: PlaceholderPage },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router