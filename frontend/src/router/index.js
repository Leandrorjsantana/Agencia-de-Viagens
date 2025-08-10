import { createRouter, createWebHistory } from 'vue-router'

// Importando as Páginas e o Layout da Área do Cliente
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import ClientAreaLayout from '../layouts/ClientAreaLayout.vue'

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
  // Adicione outras rotas públicas/placeholder aqui se necessário

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