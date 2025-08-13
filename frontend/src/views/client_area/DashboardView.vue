<template>
  <div class="dashboard-page">
    <!-- Mensagem de Carregamento -->
    <div v-if="loading" class="loading-spinner">
      <p>Carregando...</p>
    </div>

    <!-- CORREÇÃO: Adicionamos uma verificação extra (v-if) para garantir que userProfile e userProfile.profile existam -->
    <div v-if="!loading && userProfile && userProfile.profile">
      <div class="page-header">
        <!-- A saudação agora é segura -->
        <h1>Olá, {{ userProfile.profile.full_name || userProfile.username }}!</h1>
        <p>Bem-vindo ao seu painel. Aqui você pode gerenciar suas viagens e informações.</p>
      </div>

      <!-- Grade de Atalhos Rápidos -->
      <div class="dashboard-grid">
        <router-link to="/area-cliente/perfil" class="widget-card">
          <div class="widget-icon">
            <i class="fa-solid fa-user-pen"></i>
          </div>
          <div class="widget-content">
            <h3>Meu Perfil</h3>
            <p>Atualize seus dados pessoais e de contato.</p>
          </div>
        </router-link>

        <router-link to="/area-cliente/reservas" class="widget-card">
          <div class="widget-icon">
            <i class="fa-solid fa-suitcase-rolling"></i>
          </div>
          <div class="widget-content">
            <h3>Minhas Reservas</h3>
            <p>Veja o histórico e o status das suas compras.</p>
          </div>
        </router-link>

        <div class="widget-card disabled">
          <div class="widget-icon">
            <i class="fa-solid fa-tags"></i>
          </div>
          <div class="widget-content">
            <h3>Ofertas Exclusivas</h3>
            <p>Em breve: promoções especiais para você.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Mensagem de Erro -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DashboardView',
  props: {
    backendUrl: String,
  },
  data() {
    return {
      userProfile: null,
      loading: true,
      errorMessage: null,
    };
  },
  async created() {
    await this.fetchUserProfile();
  },
  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('accessToken');
      if (!token) return {};
      return { 'Authorization': `Bearer ${token}` };
    },
    async fetchUserProfile() {
      this.loading = true;
      this.errorMessage = null;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/accounts/profile/`, {
          headers: this.getAuthHeaders()
        });
        this.userProfile = response.data;
      } catch (error) {
        this.errorMessage = "Não foi possível carregar os dados do dashboard.";
        console.error("Erro ao buscar perfil para o dashboard:", error);
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.page-header {
  margin-bottom: 30px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e0e0e0;
}
.page-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #222;
  margin-bottom: 5px;
  letter-spacing: 0.03em;
}
.page-header p {
  font-size: 1rem;
  color: #555;
  margin: 0;
  font-weight: 400;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.widget-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px 18px;
  display: flex;
  align-items: center;
  gap: 15px;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  cursor: pointer;
}
.widget-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.widget-card:focus-visible {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

.widget-icon {
  font-size: 2.3rem;
  color: var(--primary-color);
  min-width: 42px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.widget-content h3 {
  margin: 0 0 4px 0;
  font-size: 1.15rem;
  font-weight: 600;
}
.widget-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.3;
}

.widget-card.disabled {
  background-color: #f1f3f5;
  cursor: not-allowed;
  opacity: 0.5;
  pointer-events: none;
}
.widget-card.disabled:hover {
  transform: none;
  box-shadow: none;
}

.error-message {
  color: #b91c1c;
  background-color: #fee2e2;
  padding: 12px 16px;
  border-radius: 6px;
  font-weight: 600;
  margin-top: 10px;
  text-align: center;
  user-select: none;
}

/* Loading spinner */
.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 0;
}
.loading-spinner p {
  font-size: 1rem;
  color: #666;
  position: relative;
  padding-left: 35px;
  font-weight: 500;
}

/* Spinner animation */
.loading-spinner p::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  width: 25px;
  height: 25px;
  margin-top: -12.5px;
  border: 3px solid var(--primary-color);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsividade */
@media (max-width: 480px) {
  .page-header h1 {
    font-size: 1.5rem;
  }
  .dashboard-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  .widget-card {
    padding: 16px 14px;
    gap: 12px;
  }
  .widget-icon {
    font-size: 2rem;
    min-width: 38px;
  }
  .widget-content h3 {
    font-size: 1.05rem;
  }
  .widget-content p {
    font-size: 0.85rem;
  }
}

</style>