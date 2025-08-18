<template>
  <div class="profile-page">
    <div class="page-header">
      <h1>Meu Perfil</h1>
      <p>Atualize as suas informações pessoais e de contato.</p>
    </div>

    <div v-if="loading" class="loading-spinner"><p>A carregar perfil...</p></div>

    <form v-if="!loading && userProfile" @submit.prevent="saveProfile" class="profile-form">
      <div class="form-grid">
        <!-- Coluna da Esquerda: Foto e Login -->
        <div class="left-column">
          <div class="profile-picture-section">
            <label>Foto de Perfil</label>
            <div class="avatar-uploader">
              <img :src="avatarPreview" alt="Avatar do Utilizador">
              <input type="file" @change="handleFileChange" accept="image/*" id="avatar-input" class="file-input">
              <label for="avatar-input" class="upload-button">
                <i class="fa-solid fa-camera"></i> Alterar Foto
              </label>
            </div>
          </div>
          <div class="form-field">
            <label>Nome de Usuário</label>
            <input type="text" :value="userProfile.username" disabled>
          </div>
          <div class="form-field">
            <label for="email">E-mail</label>
            <input type="email" id="email" v-model="userProfile.email" required>
          </div>
        </div>

        <!-- Coluna da Direita: Dados Pessoais e Endereço -->
        <div class="right-column">
          <div class="form-field">
            <label for="full_name">Nome Completo</label>
            <input type="text" id="full_name" v-model="userProfile.profile.full_name" required>
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="cpf">CPF</label>
              <input type="text" id="cpf" v-model="userProfile.profile.cpf">
            </div>
            <div class="form-field">
              <label for="phone_number">Telefone / WhatsApp</label>
              <input type="tel" id="phone_number" v-model="userProfile.profile.phone_number">
            </div>
          </div>
          <hr>
          <div class="form-field">
            <label for="cep">CEP</label>
            <input type="text" id="cep" v-model="userProfile.profile.cep" @input="handleCepInput">
          </div>
          <div class="form-field">
            <label for="logradouro">Logradouro</label>
            <input type="text" id="logradouro" v-model="userProfile.profile.logradouro">
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="numero">Número</label>
              <input type="text" id="numero" v-model="userProfile.profile.numero">
            </div>
            <div class="form-field">
              <label for="bairro">Bairro</label>
              <input type="text" id="bairro" v-model="userProfile.profile.bairro">
            </div>
          </div>
          <div class="form-row">
            <div class="form-field">
              <label for="cidade">Cidade</label>
              <input type="text" id="cidade" v-model="userProfile.profile.cidade">
            </div>
            <div class="form-field">
              <label for="estado">Estado (UF)</label>
              <input type="text" id="estado" v-model="userProfile.profile.estado">
            </div>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="save-button" :disabled="isSaving">
          {{ isSaving ? 'A salvar...' : 'Salvar Alterações' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL, getMediaUrl } from '../../config';

export default {
  name: 'ProfileView',
  data() {
    return {
      userProfile: null,
      loading: true,
      isSaving: false,
      selectedFile: null,
      avatarPreview: null,
      backendUrl: BACKEND_URL,
    };
  },
  async created() {
    await this.fetchProfile();
  },
  methods: {
    getMediaUrl,
    getAuthHeaders() {
      const token = localStorage.getItem('accessToken');
      return { 'Authorization': `Bearer ${token}` };
    },
    async fetchProfile() {
      this.loading = true;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/accounts/profile/`, { headers: this.getAuthHeaders() });
        this.userProfile = response.data;
        this.avatarPreview = this.userProfile.profile.profile_picture 
          ? this.getMediaUrl(this.userProfile.profile.profile_picture)
          : '/default-avatar.png'; // Imagem padrão
      } catch (error) {
        console.error("Erro ao buscar perfil:", error);
      } finally {
        this.loading = false;
      }
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.avatarPreview = URL.createObjectURL(file);
      }
    },
    async handleCepInput() {
      let cep = this.userProfile.profile.cep.replace(/\D/g, '');
      if (cep.length === 8) {
        try {
          const response = await axios.get(`https://viacep.com.br/ws/${cep}/json/`);
          if (!response.data.erro) {
            this.userProfile.profile.logradouro = response.data.logradouro;
            this.userProfile.profile.bairro = response.data.bairro;
            this.userProfile.profile.cidade = response.data.localidade;
            this.userProfile.profile.estado = response.data.uf;
          }
        } catch (error) {
          console.error("Erro ao buscar CEP:", error);
        }
      }
    },
    async saveProfile() {
      this.isSaving = true;
      const formData = new FormData();
      
      // Adiciona os campos de texto
      formData.append('email', this.userProfile.email);
      formData.append('profile.full_name', this.userProfile.profile.full_name);
      formData.append('profile.cpf', this.userProfile.profile.cpf);
      formData.append('profile.phone_number', this.userProfile.profile.phone_number);
      formData.append('profile.cep', this.userProfile.profile.cep);
      formData.append('profile.logradouro', this.userProfile.profile.logradouro);
      formData.append('profile.numero', this.userProfile.profile.numero);
      formData.append('profile.bairro', this.userProfile.profile.bairro);
      formData.append('profile.cidade', this.userProfile.profile.cidade);
      formData.append('profile.estado', this.userProfile.profile.estado);
      
      // Adiciona a foto, se uma nova foi selecionada
      if (this.selectedFile) {
        formData.append('profile.profile_picture', this.selectedFile);
      }

      try {
        const headers = this.getAuthHeaders();
        headers['Content-Type'] = 'multipart/form-data';
        await axios.patch(`${this.backendUrl}/api/v1/accounts/profile/`, formData, { headers });
        alert('Perfil atualizado com sucesso!');
        await this.fetchProfile(); // Recarrega os dados para mostrar a nova foto
      } catch (error) {
        alert('Ocorreu um erro ao salvar o perfil.');
        console.error("Erro ao salvar perfil:", error.response.data);
      } finally {
        this.isSaving = false;
      }
    }
  }
};
</script>

<style scoped>
.page-header { text-align: center; margin-bottom: 30px; }
.profile-form { background: #fff; padding: 30px; border-radius: 8px; }
.form-grid { display: grid; grid-template-columns: 1fr; gap: 40px; }
@media (min-width: 768px) { .form-grid { grid-template-columns: 1fr 2fr; } }
.profile-picture-section { text-align: center; margin-bottom: 20px; }
.avatar-uploader { position: relative; width: 150px; height: 150px; margin: 0 auto; }
.avatar-uploader img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; border: 3px solid #eee; }
.file-input { display: none; }
.upload-button { position: absolute; bottom: 5px; right: 5px; background: var(--primary-color); color: #fff; border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.form-field { margin-bottom: 15px; }
.form-field label { display: block; font-weight: 500; margin-bottom: 5px; }
.form-field input { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
.form-field input:disabled { background: #f4f4f4; }
.form-row { display: flex; gap: 20px; }
.form-actions { text-align: right; margin-top: 30px; }
.save-button { background: var(--primary-color); color: #fff; padding: 12px 25px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; }
</style>
