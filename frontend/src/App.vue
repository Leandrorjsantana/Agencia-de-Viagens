<template>
  <div id="app">
    <component :is="'style'" v-if="pageData?.site_configuration">
      :root {
        --primary-color: {{ pageData.site_configuration.primary_color }};
        --main-font: '{{ pageData.site_configuration.main_font }}', sans-serif;
        
        --top-bar-bg-color: {{ pageData.site_configuration.top_bar_bg_color }};
        --top-bar-text-color: {{ pageData.site_configuration.top_bar_text_color }};

        --main-header-bg-color: {{ pageData.site_configuration.main_header_bg_color }};
        --main-header-text-color: {{ pageData.site_configuration.main_header_text_color }};

        --footer-bg-color: {{ pageData.site_configuration.footer_bg_color }};
        --footer-text-color: {{ pageData.site_configuration.footer_text_color }};
      }
    </component>

    <header class="main-header" v-if="!isClientArea && pageData">
      <div class="header-top">
        <div class="container">
          <div class="top-info">
            <component v-for="link in pageData.top_bar_links" :key="link.id" :is="link.url ? 'a' : 'div'" :href="link.url || null" target="_blank" rel="noopener noreferrer" class="info-item">
              <i :class="link.icon_class"></i>
              <span>{{ link.title }}</span>
            </component>
          </div>
        </div>
      </div>
      <div class="header-main">
        <div class="container">
          <router-link to="/" class="logo">
            <img v-if="pageData.site_configuration.logo" :src="logoUrl" alt="Logo da Agência" :style="{ height: pageData.site_configuration.logo_height + 'px' }">
          </router-link>
          <nav class="main-navigation">
            <ul>
              <li v-for="item in pageData.main_menu_items" :key="item.id">
                <router-link :to="item.url">{{ item.title }}</router-link>
              </li>
            </ul>
          </nav>
          <div class="user-nav">
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
      <div v-else class="loading-container">
        <p>Carregando Agência...</p>
      </div>
    </main>

    <footer class="main-footer" v-if="!isClientArea && pageData?.site_configuration">
      <div class="container">
        <div class="social-icons" v-if="pageData.social_media_links && pageData.social_media_links.length">
          <a v-for="social in pageData.social_media_links" :key="social.id" :href="social.url" target="_blank" rel="noopener noreferrer">
            <i :class="social.icon_class"></i>
          </a>
        </div>
        <p>{{ pageData.site_configuration.footer_text }}</p>
      </div>
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
      isLoggedIn: false,
    };
  },
  computed: {
    logoUrl() { return this.pageData?.site_configuration?.logo ? `${this.backendUrl}${this.pageData.site_configuration.logo}` : ''; },
    isClientArea() {
      return this.$route.matched.some(record => record.meta.isClientArea);
    }
  },
  methods: {
    async fetchSiteData() {
      this.loading = true;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/site-data/`);
        this.pageData = response.data;
      } catch (error) { console.error("Erro ao buscar dados do site:", error); }
      finally { this.loading = false; }
    },
    checkLoginStatus() { this.isLoggedIn = !!localStorage.getItem('accessToken'); },
    updatePageMetadata(config) {
      if (!config) return;
      if (config.seo_title) document.title = config.seo_title;
      if (config.favicon) {
        const faviconTag = document.getElementById('favicon');
        if (faviconTag) faviconTag.href = `${this.backendUrl}${config.favicon}`;
      }
    }
  },
  watch: {
    pageData(newData) { this.updatePageMetadata(newData?.site_configuration); },
    '$route'() { this.checkLoginStatus(); }
  },
  created() {
    this.fetchSiteData();
    this.checkLoginStatus();
  }
};
</script>

<style>
body { font-family: var(--main-font, sans-serif); margin: 0; background-color: #f4f5f7; }
#app { display: flex; flex-direction: column; min-height: 100vh; }
.body-wrapper { flex-grow: 1; display: flex; flex-direction: column; }
.body-wrapper > * { flex-grow: 1; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
.loading-container { display: flex; justify-content: center; align-items: center; flex-grow: 1; }
.main-header { background-color: var(--main-header-bg-color); box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.header-top { background-color: var(--top-bar-bg-color); color: var(--top-bar-text-color); border-bottom: 1px solid #e9ecef; padding: 8px 0; font-size: 0.85rem; }
.top-info { display: flex; justify-content: flex-end; align-items: center; gap: 25px; }
.info-item { display: flex; align-items: center; gap: 8px; color: inherit; text-decoration: none; }
.header-main .container { display: flex; align-items: center; gap: 20px; padding: 15px 0; }
.logo img { width: auto; display: block; }
.main-navigation { flex-grow: 1; display: flex; justify-content: center; }
.main-navigation ul { display: flex; gap: 30px; list-style: none; margin: 0; padding: 0; }
.main-navigation a { text-decoration: none; color: var(--main-header-text-color); font-weight: 500; transition: color 0.2s ease-in-out; }
.main-navigation a:hover, .main-navigation a.router-link-exact-active { color: var(--primary-color); }
.user-nav { flex-shrink: 0; }
.login-button { background-color: var(--primary-color); color: #fff !important; padding: 10px 15px; border-radius: 5px; font-weight: bold; text-decoration: none; }
/* --- ESTILO APRIMORADO PARA O BOTÃO "MINHA CONTA" --- */
.client-area-button {
  background: linear-gradient(45deg, #28a745, #20c997);
  color: #fff !important;
  padding: 10px 20px;
  border-radius: 50px;
  font-weight: bold;
  text-decoration: none;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
  transition: all 0.3s ease;
}
.client-area-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 7px 20px rgba(40, 167, 69, 0.5);
}
.main-footer { background-color: var(--footer-bg-color); color: var(--footer-text-color); padding: 40px 0; text-align: center; }
.social-icons { margin-bottom: 20px; }
.social-icons a { color: #fff; font-size: 1.5rem; margin: 0 10px; transition: color 0.3s; }
.social-icons a:hover { color: var(--primary-color); }
</style>