import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import ClientAreaLayout from '../layouts/ClientAreaLayout.vue'
import OfferDetailView from '../views/OfferDetailView.vue'
import ServiceOffersView from '../views/ServiceOffersView.vue'
import ContactView from '../views/ContactView.vue'
import PageView from '../views/PageView.vue'
import AboutUsView from '../views/AboutUsView.vue' // Import adicionado

const requireAuth = (to, from, next) => {
  if (!localStorage.getItem('accessToken')) {
    next({ name: 'login' });
  } else {
    next();
  }
};

const routes = [
  // Rotas Principais e Específicas (têm prioridade)
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/ofertas/:slug', name: 'offer-detail', component: OfferDetailView },
  { path: '/ofertas/servico/:slug', name: 'service-offers', component: ServiceOffersView },
  { path: '/contato', name: 'contact', component: ContactView },
  { path: '/quem-somos', name: 'about-us', component: AboutUsView }, // Rota adicionada
  
  // --- CORREÇÃO AQUI: A rota da Área do Cliente foi movida para cima ---
  // para que seja encontrada antes da rota genérica.
  {
    path: '/area-cliente',
    component: ClientAreaLayout,
    beforeEnter: requireAuth,
    meta: { isClientArea: true },
    children: [
      { path: '', redirect: '/area-cliente/dashboard' },
      { path: 'dashboard', name: 'dashboard', component: () => import('../views/client_area/DashboardView.vue') },
      { path: 'perfil', name: 'profile', component: () => import('../views/client_area/ProfileView.vue') },
      { path: 'reservas', name: 'reservations', component: () => import('../views/client_area/ReservationsView.vue') },
    ]
  },

  // --- ROTA GENÉRICA (FICA NO FINAL) ---
  // Esta rota só será usada se nenhuma das rotas acima corresponder.
  { path: '/:slug', name: 'page', component: PageView },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
