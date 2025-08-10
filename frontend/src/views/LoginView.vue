<template>
  <div class="auth-page">
    <div class="auth-container" style="max-width: 450px;">
      <div class="auth-header">
        <h2>Acesse sua Conta</h2>
        <p>Bem-vindo de volta!</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-field">
          <label for="login">E-mail ou Nome de Usuário</label>
          <input type="text" id="login" v-model="login" required>
        </div>
        <div class="form-field">
          <label for="password">Senha</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        
        <div v-if="errorMessage" class="error-message">
          <p>{{ errorMessage }}</p>
        </div>

        <button type="submit" class="submit-button">Entrar</button>
      </form>

      <div class="auth-switch">
        <span>Não tem uma conta? <router-link to="/register">Cadastre-se</router-link></span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginView',
  props: {
    backendUrl: String,
  },
  data() {
    return {
      login: '',
      password: '',
      errorMessage: null,
    };
  },
  methods: {
    async handleLogin() {
      this.errorMessage = null;
      try {
        const payload = {
          login: this.login,
          password: this.password,
        };

        const response = await axios.post(`${this.backendUrl}/api/v1/auth/login/`, payload);
        
        // --- CORREÇÃO AQUI: Procurando pela chave 'access' do JWT ---
        if (response.data.access) {
          localStorage.setItem('accessToken', response.data.access);
          localStorage.setItem('refreshToken', response.data.refresh);
          
          alert("Login realizado com sucesso!");
          this.$router.push('/');
        } else {
          this.errorMessage = "Resposta de login inválida do servidor.";
        }
      } catch (error) {
        if (error.response && error.response.data) {
          const errors = error.response.data.non_field_errors || [error.response.data.detail];
          this.errorMessage = errors ? errors.join(', ') : "Credenciais inválidas.";
        } else {
          this.errorMessage = "Não foi possível conectar ao servidor.";
        }
        console.error("Erro no login:", error);
      }
    }
  }
};
</script>

<style scoped>
.auth-page { padding: 60px 20px; background-color: #f4f5f7; }
.auth-container { max-width: 600px; margin: 0 auto; background: #fff; padding: 40px; border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.1); }
.auth-header { text-align: center; margin-bottom: 30px; }
.form-field { margin-bottom: 20px; }
.form-field label { display: block; font-weight: 500; margin-bottom: 8px; }
.form-field input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 5px; font-size: 1rem; }
.submit-button { width: 100%; padding: 15px; font-size: 1.1rem; font-weight: bold; color: #fff; background-color: var(--primary-color); border: none; border-radius: 8px; cursor: pointer; transition: opacity 0.3s; }
.error-message { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
.auth-switch { text-align: center; margin-top: 25px; }
</style>