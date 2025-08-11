import { createRouter, createWebHistory } from 'vue-router'

// Importando as Páginas e o Layout da Área do Cliente
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import ClientAreaLayout from '../layouts/ClientAreaLayout.vue'

// Componente genérico para páginas em construção
const PlaceholderPage = { template: '<div class="container" style="padding: 50px 20px;"><h2>Página em Construção</h2><p>O conteúdo para esta seção estará disponível em breve.</p></div>' };

// Função de "guarda" que protege as rotas
const requireAuth = (to, from, next) => {
  if (!localStorage.getItem('accessToken')) {
    next({ name: 'login' });
  } else {
    next();
  }
};

const routes = [
  // Rotas Públicas
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/experiencias', name: 'experiencias', component: PlaceholderPage },
  { path: '/destinos', name: 'destinos', component: PlaceholderPage },
  { path: '/servicos', name: 'servicos', component: PlaceholderPage },
  { path: '/blog', name: 'blog', component: PlaceholderPage },
  { path: '/sobre-nos', name: 'sobre-nos', component: PlaceholderPage },
  { path: '/contato', name: 'contato', component: PlaceholderPage },
  { path: '/ajuda', name: 'ajuda', component: PlaceholderPage },
  { path: '/televendas', name: 'televendas', component: PlaceholderPage },
  { path: '/ofertas/:slug', name: 'offer-detail', component: PlaceholderPage },
  { path: '/ofertas/servico/:slug', name: 'service-offers', component: PlaceholderPage },

  // Rotas da Área do Cliente
  {
    path: '/area-cliente',
    component: ClientAreaLayout,
    beforeEnter: requireAuth,
    // A mágica está aqui: esta "meta" informação diz ao App.vue para se esconder
    meta: { isClientArea: true },
    children: [
      { path: '', redirect: '/area-cliente/dashboard' },
      { path: 'dashboard', name: 'dashboard', component: () => import('../views/client_area/DashboardView.vue') },
      { path: 'perfil', name: 'profile', component: () => import('../views/client_area/ProfileView.vue') },
      { path: 'reservas', name: 'reservations', component: () => import('../views/client_area/ReservationsView.vue') },
    ]
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router