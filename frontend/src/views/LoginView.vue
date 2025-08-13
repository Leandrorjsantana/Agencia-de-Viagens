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
import { BACKEND_URL } from '../config';

export default {
  name: 'LoginView',
  data() {
    return {
      login: '',
      password: '',
      errorMessage: null,
      backendUrl: BACKEND_URL,
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

        if (response.data.access) {
          localStorage.setItem('accessToken', response.data.access);
          localStorage.setItem('refreshToken', response.data.refresh);
          
          alert("Login realizado com sucesso!");

          // --- A MÁGICA ACONTECE AQUI ---
          // 1. Verificamos se existe uma página de redirecionamento na URL.
          const redirectPath = this.$route.query.redirect;

          if (redirectPath) {
            // 2. Se existir, enviamos o cliente de volta para lá.
            this.$router.push(redirectPath);
          } else {
            // 3. Se não, enviamos para a página inicial, como antes.
            this.$router.push('/');
          }
          // --- FIM DA MÁGICA ---

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
.auth-page {
  padding: 60px 20px;
  min-height: 100vh;
  background-color: #f9fafb; /* fundo brando e claro */
  display: flex;
  justify-content: center;
  align-items: center;
}

.auth-container {
  max-width: 400px;
  width: 100%;
  background: #fff;
  padding: 40px 35px;
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1); /* sombra suave */
  transition: transform 0.3s ease;
}

.auth-container:hover {
  transform: translateY(-5px);
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h2 {
  font-weight: 700;
  font-size: 2rem;
  color: #333;
  margin-bottom: 6px;
}

.auth-header p {
  color: #666;
  font-size: 1rem;
  font-weight: 500;
}

.form-field {
  margin-bottom: 20px;
}

.form-field label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #444;
  font-size: 1rem;
}

.form-field input {
  width: 100%;
  padding: 14px 15px;
  border: 2px solid #ddd;
  border-radius: 12px;
  font-size: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  outline: none;
  box-sizing: border-box;
  height: 48px; /* altura igual ao botão */
}

.form-field input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 8px var(--primary-color);
}

.submit-button {
  width: 100%;
  padding: 0;
  height: 48px; /* altura alinhada aos inputs */
  font-size: 1.15rem;
  font-weight: 700;
  color: #fff;
  background-color: var(--primary-color);
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.submit-button:hover {
  background-color: #5a67d8;
}

.error-message {
  background-color: #fdecea;
  color: #b92c28;
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.95rem;
}

.error-message p {
  margin: 0;
}

.error-message::before {
  content: "⚠️";
}

.auth-switch {
  text-align: center;
  margin-top: 25px;
  font-size: 0.95rem;
  color: #555;
}

.auth-switch a {
  color: var(--primary-color);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

.auth-switch a:hover {
  text-decoration: underline;
  color: #5a67d8;
}

@media (max-width: 480px) {
  .auth-container {
    padding: 30px 25px;
    border-radius: 12px;
  }
  .auth-header h2 {
    font-size: 1.75rem;
  }
  .submit-button {
    font-size: 1rem;
    height: 44px;
  }
  .form-field input {
    height: 44px;
  }
}
</style>