import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import ClientAreaLayout from '../layouts/ClientAreaLayout.vue'
import OfferDetailView from '../views/OfferDetailView.vue'
import ServiceOffersView from '../views/ServiceOffersView.vue'
import ContactView from '../views/ContactView.vue'
import PageView from '../views/PageView.vue'
import BlogView from '../views/BlogView.vue'
import PostDetailView from '../views/PostDetailView.vue'
import AboutUsView from '../views/AboutUsView.vue'
import CategoryBlogView from '../views/CategoryBlogView.vue'
import ExperiencesView from '../views/ExperiencesView.vue'
import HelpCenterView from '../views/HelpCenterView.vue'
// Importando a nossa nova página
import InsuranceView from '../views/InsuranceView.vue'

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
  { path: '/quem-somos', name: 'about-us', component: AboutUsView },
  { path: '/experiencias', name: 'experiencias', component: ExperiencesView },
  { path: '/blog', name: 'blog', component: BlogView },
  { path: '/blog/:slug', name: 'post-detail', component: PostDetailView },
  { path: '/blog/categoria/:slug', name: 'category-blog', component: CategoryBlogView },
  { path: '/ajuda', name: 'help-center', component: HelpCenterView },
  
  // --- ROTA DE SEGURO VIAGEM ADICIONADA AQUI ---
  { path: '/seguro-viagem', name: 'insurance', component: InsuranceView },

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
      { path: 'avaliacoes', name: 'my-reviews', component: () => import('../views/client_area/MyReviewsView.vue') },
      { path: 'avaliacoes/nova', name: 'submit-review', component: () => import('../views/client_area/SubmitReviewView.vue') },
    ]
  },

  // Rota genérica para páginas de conteúdo (fica no final)
  { path: '/:slug', name: 'page', component: PageView },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router