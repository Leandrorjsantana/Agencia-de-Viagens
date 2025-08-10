import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import ClientAreaLayout from '../layouts/ClientAreaLayout.vue'

// Função de "guarda" que verifica se o usuário está logado
const requireAuth = (to, from, next) => {
  if (!localStorage.getItem('accessToken')) {
    // Se não houver token, redireciona para a página de login
    next({ name: 'login' });
  } else {
    // Se houver token, permite o acesso
    next();
  }
};

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/login', name: 'login', component: LoginView },

  // --- NOVA SEÇÃO DE ROTAS PROTEGIDAS ---
  {
    path: '/area-cliente',
    component: ClientAreaLayout,
    beforeEnter: requireAuth, // O "guarda" é aplicado aqui
    children: [
      {
        // Redireciona /area-cliente para /area-cliente/dashboard
        path: '',
        redirect: '/area-cliente/dashboard'
      },
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('../views/client_area/DashboardView.vue')
      },
      {
        path: 'perfil',
        name: 'profile',
        component: () => import('../views/client_area/ProfileView.vue')
      },
      {
        path: 'reservas',
        name: 'reservations',
        component: () => import('../views/client_area/ReservationsView.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router