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
  margin-bottom: 40px;
}
.page-header h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #333;
}
.page-header p {
  font-size: 1.1rem;
  color: #666;
}
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}
.widget-card {
  background-color: #fff;
  border-radius: 12px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}
.widget-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}
.widget-icon {
  font-size: 2.5rem;
  color: var(--primary-color);
}
.widget-content h3 {
  margin: 0 0 5px 0;
  font-size: 1.2rem;
}
.widget-content p {
  margin: 0;
  color: #777;
}
.widget-card.disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
  opacity: 0.6;
}
.widget-card.disabled:hover {
  transform: none;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.error-message {
  color: #721c24;
  background-color: #f8d7da;
  padding: 15px;
  border-radius: 5px;
}
</style>