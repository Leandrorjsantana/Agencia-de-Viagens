<template>
  <div id="app">
    <!-- Cor primária dinâmica -->
    <component :is="'style'" v-if="pageData?.site_configuration?.primary_color">
      :root {
        --primary-color: {{ pageData.site_configuration.primary_color }};
      }
    </component>

    <!-- Cabeçalho -->
    <header class="main-header" v-if="pageData">
      <div class="header-top">
        <div class="container">
          <div class="top-info">
            <!-- Links do topo -->
            <component
              v-for="link in pageData.top_bar_links"
              :key="link.id"
              :is="link.url ? 'a' : 'div'"
              :href="link.url || null"
              target="_blank"
              rel="noopener noreferrer"
              class="info-item"
            >
              <i :class="link.icon_class"></i>
              <span>{{ link.title }}</span>
            </component>
          </div>
        </div>
      </div>
      <div class="header-main">
        <div class="container">
          <router-link to="/" class="logo">
            <img
              v-if="pageData.site_configuration.logo"
              :src="logoUrl"
              alt="Logo da Agência"
              :style="{ height: pageData.site_configuration.logo_height + 'px' }"
            >
          </router-link>
          <nav class="main-navigation">
            <ul>
              <li v-for="item in pageData.main_menu_items" :key="item.id">
                <router-link :to="item.url">{{ item.title }}</router-link>
              </li>
            </ul>
          </nav>
          <div class="user-nav">
            <router-link to="/login" class="login-button">Entrar / Cadastrar</router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Conteúdo principal -->
    <main class="body-wrapper">
      <router-view
        v-if="!loading"
        :pageData="pageData"
        :backendUrl="backendUrl"
      />
      <div v-else class="loading-container">
        <p>Carregando Agência...</p>
      </div>
    </main>

    <!-- Rodapé -->
    <footer class="main-footer" v-if="pageData?.site_configuration">
      <div class="container">
        <p>{{ pageData.site_configuration.footer_text }}</p>
      </div>
    </footer>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      pageData: null,
      loading: true,
      backendUrl: "http://127.0.0.1:8000", // CORRIGIDO - URL limpa
    };
  },
  computed: {
    logoUrl() {
      if (this.pageData?.site_configuration?.logo) {
        return `${this.backendUrl}${this.pageData.site_configuration.logo}`;
      }
      return "";
    },
  },
  methods: {
    async fetchSiteData() {
      this.loading = true;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/site-data/`);
        this.pageData = response.data;
      } catch (error) {
        console.error("Erro ao buscar dados do site:", error);
      } finally {
        this.loading = false;
      }
    },
  },
  created() {
    this.fetchSiteData();
  },
};
</script>

<style>
:root {
  --primary-color: #0d6efd;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  background-color: #f4f5f7;
  color: #333;
  line-height: 1.6;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.body-wrapper {
  flex-grow: 1;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.loading-container {
  text-align: center;
  padding: 50px;
  font-size: 1.2rem;
}

/* Cabeçalho */
.main-header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.header-top {
  border-bottom: 1px solid #e9ecef;
  padding: 8px 0;
  font-size: 0.85rem;
}
.top-info {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 25px;
}
.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: inherit;
  text-decoration: none;
}
.header-main .container {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px 0;
}
.logo img {
  width: auto;
  display: block;
}
.main-navigation {
  flex-grow: 1;
  display: flex;
  justify-content: center;
}
.main-navigation ul {
  display: flex;
  gap: 30px;
  list-style: none;
  margin: 0;
  padding: 0;
}
.main-navigation a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
}
.user-nav {
  flex-shrink: 0;
}
.login-button {
  background-color: var(--primary-color);
  color: #fff !important;
  padding: 10px 15px;
  border-radius: 5px;
  font-weight: bold;
  text-decoration: none;
}

/* Rodapé */
.main-footer {
  background-color: #212529;
  color: #fff;
  padding: 40px 0;
  text-align: center;
}
</style>
