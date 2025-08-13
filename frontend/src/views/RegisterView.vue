<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h2>Crie sua Conta</h2>
        <p>É rápido e fácil. Preencha seus dados para começar.</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="auth-form">
        
        <fieldset class="form-section">
          <legend>Informações Pessoais</legend>
          <div class="form-field">
            <label for="fullName">Nome Completo</label>
            <input type="text" id="fullName" v-model="profile.full_name" required>
          </div>
          <div class="form-grid">
            <div class="form-field">
              <label for="cpf">CPF</label>
              <input type="text" id="cpf" v-model="profile.cpf" required>
            </div>
            <div class="form-field">
              <label for="phone">Telefone / WhatsApp</label>
              <input type="tel" id="phone" v-model="profile.phone_number" required>
            </div>
          </div>
        </fieldset>

        <fieldset class="form-section">
          <legend>Informações de Login</legend>
          <div class="form-field">
            <label for="username">Nome de Usuário</label>
            <input type="text" id="username" v-model="user.username" required>
          </div>
          <div class="form-field">
            <label for="email">E-mail</label>
            <input type="email" id="email" v-model="user.email" required>
          </div>
          <div class="form-grid">
            <div class="form-field">
              <label for="password">Senha</label>
              <input type="password" id="password" v-model="user.password" required>
            </div>
            <div class="form-field">
              <label for="passwordConfirm">Confirme sua Senha</label>
              <input type="password" id="passwordConfirm" v-model="passwordConfirm" required>
            </div>
          </div>
        </fieldset>
        
        <div v-if="errorMessage" class="error-message">
          <p v-for="(error, index) in errorMessages" :key="index">{{ error }}</p>
        </div>

        <button type="submit" class="submit-button">Criar Minha Conta</button>
      </form>

      <div class="auth-switch">
        <span>Já tem uma conta? <router-link to="/login">Faça login</router-link></span>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterView',
  props: {
    backendUrl: String,
  },
  data() {
    return {
      user: {
        username: '',
        email: '',
        password: '',
      },
      profile: {
        full_name: '',
        cpf: '',
        phone_number: '',
        cep: '', // Campos de endereço podem ser adicionados aqui no futuro
        logradouro: '',
        numero: '',
        bairro: '',
        cidade: '',
        estado: '',
      },
      passwordConfirm: '',
      errorMessage: null,
    };
  },
  computed: {
    errorMessages() {
      if (!this.errorMessage) return [];
      // Transforma o objeto de erro em uma lista de strings para exibição
      const messages = [];
      for (const key in this.errorMessage) {
        messages.push(`${key}: ${this.errorMessage[key].join(', ')}`);
      }
      return messages;
    }
  },
  methods: {
    async handleRegister() {
      this.errorMessage = null;

      if (this.user.password !== this.passwordConfirm) {
        this.errorMessage = { "Senhas": ["As senhas não coincidem."] };
        return;
      }
      
      const registrationData = {
        ...this.user,
        profile: this.profile
      };

      try {
        const response = await axios.post(`${this.backendUrl}/api/v1/accounts/register/`, registrationData);
        if (response.status === 201) {
          alert("Cadastro realizado com sucesso! Você será redirecionado para a página de login.");
          this.$router.push('/login');
        }
      } catch (error) {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data;
        } else {
          this.errorMessage = { "Erro": ["Não foi possível conectar ao servidor."] };
        }
        console.error("Erro no cadastro:", error);
      }
    }
  }
};
</script>

<style scoped>
/* Garantir box-sizing para todos */
*,
*::before,
*::after {
  box-sizing: border-box;
}

.auth-page {
  padding: 60px 20px;
  background-color: #f4f5f7;
}
.auth-container {
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.1);
}
.auth-header {
  text-align: center;
  margin-bottom: 30px;
}
.auth-header h2 {
  font-size: 2rem;
  color: #333;
}
.auth-header p {
  color: #666;
}
.form-section {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
}
.form-section legend {
  font-weight: 600;
  font-size: 1.1rem;
  padding: 0 10px;
  margin-left: 10px;
  color: var(--primary-color);
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
  font-weight: 500;
  margin-bottom: 8px;
}
.form-field input {
  width: 100%;
  max-width: 100%;
  padding: 14px 15px;
  font-size: 1rem;
  border-radius: 8px;
  border: 1.8px solid #ccc;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  font-weight: 400;
  box-sizing: border-box;
}
.submit-button {
  width: 100%;
  padding: 15px;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  background-color: var(--primary-color);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: opacity 0.3s;
}
.submit-button:hover {
  opacity: 0.9;
}
.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 5px;
  text-align: left;
  margin-bottom: 20px;
}
.auth-switch {
  text-align: center;
  margin-top: 25px;
}
</style>
