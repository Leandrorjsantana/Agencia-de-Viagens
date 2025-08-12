import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import ClientAreaLayout from '../layouts/ClientAreaLayout.vue'
import OfferDetailView from '../views/OfferDetailView.vue'
import ServiceOffersView from '../views/ServiceOffersView.vue'
import ContactView from '../views/ContactView.vue'

const PlaceholderPage = { template: '<div class="container" style="padding: 50px 20px;"><h2>Página em Construção</h2></div>' };

const requireAuth = (to, from, next) => {
  if (!localStorage.getItem('accessToken')) {
    next({ name: 'login' });
  } else {
    next();
  }
};

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/ofertas/:slug', name: 'offer-detail', component: OfferDetailView },
  { path: '/ofertas/servico/:slug', name: 'service-offers', component: ServiceOffersView },
  { path: '/contato', name: 'contact', component: ContactView },
  
  // Rotas placeholder para as outras páginas
  { path: '/experiencias', name: 'experiencias', component: PlaceholderPage },
  // ... (outras rotas placeholder)

  {
    path: '/area-cliente',
    component: ClientAreaLayout,
    beforeEnter: requireAuth,
    meta: { isClientArea: true },
    children: [
      // ... (rotas da área do cliente)
    ]
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router