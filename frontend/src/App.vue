<template>
  <div id="app">
    <component :is="'style'" v-if="pageData?.site_configuration?.primary_color">
      :root {
        --primary-color: {{ pageData.site_configuration.primary_color }};
      }
    </component>

    <header class="main-header" v-if="pageData">
      <div class="header-top">
        <div class="container">
          <div class="top-info">
            <a v-for="link in pageData.top_bar_links" :key="link.id" :href="link.url" class="info-item">
              <i :class="link.icon_class"></i>
              <span>{{ link.title }}</span>
            </a>
          </div>
        </div>
      </div>
      <div class="header-main">
        <div class="container">
          <router-link to="/" class="logo">
            <img v-if="pageData.site_configuration" :src="logoUrl" alt="Logo">
          </router-link>
          <nav class="main-navigation">
            <ul>
              <li v-for="item in pageData.main_menu_items" :key="item.id">
                <router-link :to="item.url">{{ item.title }}</router-link>
              </li>
            </ul>
          </nav>
          <div class="user-nav">
            <!-- LÓGICA ATUALIZADA AQUI -->
            <div v-if="isLoggedIn">
              <router-link to="/area-cliente" class="client-area-button">Minha Conta</router-link>
            </div>
            <div v-else>
              <router-link to="/login" class="login-button">Entrar / Cadastrar</router-link>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="body-wrapper">
      <router-view v-if="!loading" :pageData="pageData" :backendUrl="backendUrl" />
      <div v-else style="text-align: center; padding: 50px;">Carregando...</div>
    </main>

    <footer class="main-footer" v-if="pageData?.site_configuration">
      <p>&copy; {{ new Date().getFullYear() }} {{ pageData.site_configuration.site_name }}</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'App',
  data() {
    return {
      pageData: null,
      loading: true,
      backendUrl: "http://127.0.0.1:8000",
      isLoggedIn: false, // Novo estado para controlar o login
    };
  },
  computed: {
    logoUrl() {
      return this.pageData?.site_configuration?.logo ? `${this.backendUrl}${this.pageData.site_configuration.logo}` : '';
    },
  },
  methods: {
    async fetchSiteData() {
      this.loading = true;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/site-data/`);
        this.pageData = response.data;
      } catch (error) {
        console.error("ERRO CRÍTICO AO BUSCAR DADOS:", error);
      } finally {
        this.loading = false;
      }
    },
    // Novo método para verificar o status de login
    checkLoginStatus() {
      const token = localStorage.getItem('accessToken');
      this.isLoggedIn = !!token; // !! converte a string (ou null) para booleano
    }
  },
  created() {
    this.fetchSiteData();
    this.checkLoginStatus(); // Verifica o login quando o app é criado
  },
  // Observador que re-verifica o login toda vez que a rota muda
  watch: {
    '$route'() {
      this.checkLoginStatus();
    }
  }
};
</script>

<style>
/* Seus estilos globais aqui */
:root { --primary-color: #0d6efd; }
body { font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif; margin: 0; background-color: #f4f5f7; }
#app { display: flex; flex-direction: column; min-height: 100vh; }
.body-wrapper { flex-grow: 1; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.main-header { background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.header-top { border-bottom: 1px solid #e9ecef; padding: 8px 0; font-size: 0.85rem; }
.top-info { display: flex; justify-content: flex-end; align-items: center; gap: 25px; }
.info-item { display: flex; align-items: center; gap: 8px; color: inherit; text-decoration: none; }
.header-main .container { display: flex; align-items: center; gap: 20px; padding: 15px 0; }
.logo img { height: 50px; width: auto; }
.main-navigation { flex-grow: 1; display: flex; justify-content: center; }
.main-navigation ul { display: flex; gap: 30px; list-style: none; }
.main-navigation a { color: #333; font-weight: 500; text-decoration: none; }
.user-nav { flex-shrink: 0; }
.login-button { background-color: var(--primary-color); color: #fff !important; padding: 10px 15px; border-radius: 5px; font-weight: bold; text-decoration: none; }
.client-area-button { background-color: #198754; color: #fff !important; padding: 10px 15px; border-radius: 5px; font-weight: bold; text-decoration: none; }
.main-footer { background-color: #212529; color: #fff; padding: 40px 0; text-align: center; }
</style>