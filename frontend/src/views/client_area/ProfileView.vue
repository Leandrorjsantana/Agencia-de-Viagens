<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>Meu Perfil</h1>
      <p>Aqui você pode ver e atualizar seus dados cadastrais.</p>
    </div>

    <!-- Mensagem de Carregamento -->
    <div v-if="loading" class="loading-spinner">
      <p>Carregando seu perfil...</p>
    </div>
    
    <!-- Formulário de Perfil -->
    <form v-if="!loading && user" @submit.prevent="updateProfile" class="profile-form">
      
      <fieldset class="form-section">
        <legend>Informações de Login</legend>
        <div class="form-grid">
          <div class="form-field">
            <label for="username">Nome de Usuário</label>
            <input type="text" id="username" :value="user.username" disabled>
            <small>O nome de usuário não pode ser alterado.</small>
          </div>
          <div class="form-field">
            <label for="email">E-mail</label>
            <input type="email" id="email" v-model="user.email">
          </div>
        </div>
      </fieldset>

      <fieldset class="form-section">
        <legend>Informações Pessoais</legend>
        <div class="form-field">
          <label for="fullName">Nome Completo</label>
          <input type="text" id="fullName" v-model="user.profile.full_name">
        </div>
        <div class="form-grid">
          <div class="form-field">
            <label for="cpf">CPF</label>
            <input type="text" id="cpf" v-model="user.profile.cpf">
          </div>
          <div class="form-field">
            <label for="phone">Telefone / WhatsApp</label>
            <input type="tel" id="phone" v-model="user.profile.phone_number">
          </div>
        </div>
      </fieldset>

      <!-- Futuramente, a seção de endereço virá aqui -->

      <div class="form-actions">
        <button type="submit" class="save-button" :disabled="isSaving">
          {{ isSaving ? 'Salvando...' : 'Salvar Alterações' }}
        </button>
      </div>

      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ProfileView',
  props: {
    backendUrl: String,
  },
  data() {
    return {
      user: null,
      loading: true,
      isSaving: false,
      errorMessage: null,
      successMessage: null,
    };
  },
  async created() {
    // Busca os dados do perfil assim que a página é criada
    await this.fetchUserProfile();
  },
  methods: {
    // Método para criar os cabeçalhos de autenticação para a API
    getAuthHeaders() {
      const token = localStorage.getItem('accessToken');
      if (!token) return {};
      return {
        'Authorization': `Bearer ${token}`
      };
    },
    // Método para buscar os dados do perfil na nossa API segura
    async fetchUserProfile() {
      this.loading = true;
      this.errorMessage = null;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/accounts/profile/`, {
          headers: this.getAuthHeaders()
        });
        this.user = response.data;
      } catch (error) {
        this.errorMessage = "Erro ao carregar seu perfil. Tente recarregar a página.";
        console.error("Erro ao buscar perfil:", error);
      } finally {
        this.loading = false;
      }
    },
    // Método para enviar os dados atualizados para a API
    async updateProfile() {
      this.isSaving = true;
      this.errorMessage = null;
      this.successMessage = null;
      try {
        const payload = {
          email: this.user.email,
          profile: this.user.profile
        };
        const response = await axios.put(`${this.backendUrl}/api/v1/accounts/profile/`, payload, {
          headers: this.getAuthHeaders()
        });
        this.user = response.data;
        this.successMessage = "Perfil atualizado com sucesso!";
      } catch (error) {
        this.errorMessage = "Erro ao atualizar o perfil. Verifique os dados e tente novamente.";
        console.error("Erro ao atualizar perfil:", error);
      } finally {
        this.isSaving = false;
      }
    }
  }
};
</script>

<style scoped>
.profile-page {
  max-width: 900px;
}
.page-header {
  margin-bottom: 30px;
}
.page-header h1 {
  font-size: 2rem;
  margin-bottom: 5px;
}
.profile-form {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.form-section {
  border: none;
  padding: 0;
  margin-bottom: 25px;
}
.form-section legend {
  font-weight: 600;
  font-size: 1.2rem;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
  width: 100%;
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.form-field {
  margin-bottom: 15px;
}
.form-field label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}
.form-field input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}
.form-field input:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
}
.form-field small {
  font-size: 0.8rem;
  color: #777;
  margin-top: 5px;
}
.form-actions {
  text-align: right;
  margin-top: 30px;
}
.save-button {
  padding: 12px 25px;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: var(--primary-color);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.save-button:hover {
  opacity: 0.9;
}
.save-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.success-message, .error-message {
  margin-top: 20px;
  padding: 15px;
  border-radius: 5px;
  text-align: center;
}
.success-message { background-color: #d4edda; color: #155724; }
.error-message { background-color: #f8d7da; color: #721c24; }
</style>
