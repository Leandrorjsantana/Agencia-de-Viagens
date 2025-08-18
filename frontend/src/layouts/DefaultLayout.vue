<template>
  <div class="default-layout">
    <header class="main-header" v-if="pageData">
      <div class="header-top">
        <div class="container">
          <div class="top-info">
            <component 
              v-for="link in pageData.top_bar_links" 
              :key="link.id" 
              :is="link.url ? 'a' : 'div'" 
              :href="link.url || null" 
              :target="getTarget(link)" 
              :rel="getRel(link)"
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
      <router-view :pageData="pageData" :backendUrl="backendUrl" />
    </main>

    <footer class="main-footer" v-if="pageData?.site_configuration">
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
export default {
  name: 'DefaultLayout',
  props: ['pageData', 'backendUrl', 'isLoggedIn'],
  computed: {
    logoUrl() {
      if (this.pageData?.site_configuration?.logo) {
        return `${this.backendUrl}${this.pageData.site_configuration.logo}`;
      }
      return '';
    }
  },
  // --- MÉTODOS ADICIONADOS PARA A LÓGICA DOS LINKS ---
  methods: {
    getTarget(link) {
      // Retorna '_blank' apenas se a propriedade for explicitamente true
      return link.open_in_new_tab === true ? '_blank' : '_self';
    },
    getRel(link) {
      // Retorna o atributo 'rel' apenas se for abrir em nova aba
      return link.open_in_new_tab === true ? 'noopener noreferrer' : null;
    }
  }
}
</script>

<style scoped>
/* Estilos específicos para este layout, se necessário */
.body-wrapper {
  flex-grow: 1;
}
</style>