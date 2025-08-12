<template>
  <div class="page-container">
    <!-- Ecrã de Carregamento -->
    <div v-if="loading" class="loading-container">
      <p>A carregar página...</p>
    </div>

    <!-- Conteúdo da Página -->
    <div v-if="!loading && page" class="container page-content">
      <h1 class="page-title">{{ page.title }}</h1>
      <!-- A diretiva v-html é usada para renderizar o conteúdo formatado do CKEditor -->
      <div class="content-body" v-html="page.content"></div>
    </div>

    <!-- Mensagem de Erro -->
    <div v-if="error" class="error-message container">
      <h2>Página Não Encontrada</h2>
      <p>A página que você está a tentar aceder não foi encontrada.</p>
      <router-link to="/" class="back-home-button">Voltar à Página Inicial</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL } from '../config';

export default {
  name: 'PageView',
  data() {
    return {
      page: null,
      loading: true,
      error: false,
      backendUrl: BACKEND_URL,
    };
  },
  watch: {
    // Observa mudanças na URL para recarregar o conteúdo da página
    // Isto é crucial para que os links do menu funcionem corretamente
    '$route.params.slug': {
      immediate: true,
      handler() {
        this.fetchPageContent();
      }
    }
  },
  methods: {
    async fetchPageContent() {
      this.loading = true;
      this.error = false;
      // Pega o 'slug' da página diretamente da URL
      const slug = this.$route.params.slug;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/pages/${slug}/`);
        this.page = response.data;

        // Atualiza o título e a descrição da aba do navegador (SEO)
        if (this.page.seo_title) {
          document.title = this.page.seo_title;
        } else {
          document.title = this.page.title;
        }
        
        const descriptionTag = document.querySelector('meta[name="description"]');
        if (descriptionTag && this.page.seo_description) {
          descriptionTag.setAttribute('content', this.page.seo_description);
        }

      } catch (err) {
        this.error = true;
        console.error("Erro ao buscar conteúdo da página:", err);
      } finally {
        this.loading = false;
      }
    },
  }
};
</script>

<style scoped>
.page-container {
  padding: 60px 0;
  background-color: #fff;
  flex-grow: 1;
}
.page-content {
  max-width: 800px; /* Limita a largura para melhor legibilidade */
}
.page-title {
  font-size: 2.5rem;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid var(--primary-color);
}
.content-body {
  line-height: 1.8;
  font-size: 1.1rem;
  color: #333;
}
/* Estiliza o conteúdo que vem do CKEditor */
.content-body ::v-deep(p) {
  margin-bottom: 1.2em;
}
.content-body ::v-deep(h2) {
  font-size: 1.8rem;
  margin-top: 1.5em;
  margin-bottom: 0.8em;
}
.content-body ::v-deep(ul),
.content-body ::v-deep(ol) {
  padding-left: 25px;
  margin-bottom: 1.2em;
}
.error-message {
  text-align: center;
  padding: 50px;
}
.back-home-button {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 25px;
  background-color: var(--primary-color);
  color: #fff;
  border-radius: 50px;
  text-decoration: none;
  font-weight: bold;
}
</style>