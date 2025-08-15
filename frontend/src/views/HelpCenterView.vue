<template>
  <div class="help-center-page">
    <div class="page-header">
      <div class="container">
        <h1>Central de Ajuda</h1>
        <p>Encontre respostas para as suas dúvidas mais frequentes.</p>
        <div class="search-bar">
          <input type="text" placeholder="Escreva uma palavra-chave (ex: cancelamento, bagagem)">
          <button><i class="fa-solid fa-magnifying-glass"></i></button>
        </div>
      </div>
    </div>

    <div class="container page-content">
      <div v-if="loading" class="loading-spinner"><p>A carregar...</p></div>
      
      <div v-if="!loading && categories.length > 0" class="help-layout">
        <!-- Coluna da Esquerda: Menu de Categorias -->
        <aside class="sidebar">
          <nav>
            <ul>
              <li v-for="category in categories" :key="category.id">
                <a 
                  href="#" 
                  @click.prevent="activeCategoryId = category.id" 
                  :class="{ active: activeCategoryId === category.id }"
                >
                  <i :class="category.icon_class"></i>
                  <span>{{ category.title }}</span>
                </a>
              </li>
            </ul>
          </nav>
        </aside>

        <!-- Coluna da Direita: Artigos -->
        <main class="main-content">
          <div v-if="activeCategory">
            <h2>{{ activeCategory.title }}</h2>
            <div class="accordion">
              <div v-for="article in activeCategory.articles" :key="article.id" class="accordion-item">
                <button class="accordion-header" @click="toggleArticle(article.id)">
                  <span>{{ article.question }}</span>
                  <i class="fa-solid" :class="isOpen(article.id) ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
                </button>
                <div v-if="isOpen(article.id)" class="accordion-body" v-html="article.answer"></div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL } from '../config';

export default {
  name: 'HelpCenterView',
  data() {
    return {
      categories: [],
      loading: true,
      activeCategoryId: null,
      openArticleIds: [], // Guarda os IDs dos artigos abertos
    };
  },
  computed: {
    activeCategory() {
      if (!this.activeCategoryId) return null;
      return this.categories.find(cat => cat.id === this.activeCategoryId);
    }
  },
  methods: {
    async fetchHelpData() {
      this.loading = true;
      try {
        const response = await axios.get(`${BACKEND_URL}/api/v1/help-center/`);
        this.categories = response.data;
        if (this.categories.length > 0) {
          this.activeCategoryId = this.categories[0].id;
        }
      } catch (error) {
        console.error("Erro ao buscar dados da Central de Ajuda:", error);
      } finally {
        this.loading = false;
      }
    },
    toggleArticle(articleId) {
      const index = this.openArticleIds.indexOf(articleId);
      if (index > -1) {
        this.openArticleIds.splice(index, 1); // Fecha se já estiver aberto
      } else {
        this.openArticleIds.push(articleId); // Abre se estiver fechado
      }
    },
    isOpen(articleId) {
      return this.openArticleIds.includes(articleId);
    }
  },
  created() {
    this.fetchHelpData();
  }
};
</script>

<style scoped>
.page-header {
  padding: 40px 0;
  background-color: #003366;
  color: #fff;
  text-align: center;
}
.page-header h1 { font-size: 2rem; }
.search-bar {
  max-width: 500px;
  margin: 20px auto 0;
  display: flex;
}
.search-bar input {
  flex-grow: 1;
  padding: 10px;
  border: none;
  border-radius: 50px 0 0 50px;
  font-size: 0.9rem;
}
.search-bar button {
  padding: 0 20px;
  border: none;
  background: #fff;
  color: var(--primary-color);
  border-radius: 0 50px 50px 0;
  cursor: pointer;
  font-size: 1rem;
}

.page-content { padding: 30px 15px; }
.help-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}
@media (min-width: 768px) {
  .help-layout { grid-template-columns: 1fr 2.5fr; }
}

.sidebar nav ul { list-style: none; padding: 0; margin: 0; }
.sidebar nav a {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
  font-weight: 500;
  margin-bottom: 5px;
}
.sidebar nav a:hover { background-color: #f0f2f5; }
.sidebar nav a.active { background-color: var(--primary-color); color: #fff; }

.main-content h2 { font-size: 1.5rem; margin-bottom: 15px; }
.accordion-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  margin-bottom: 10px;
}
.accordion-header {
  background: #fff;
  width: 100%;
  padding: 10px 12px;
  border: none;
  text-align: left;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.accordion-body {
  padding: 0 12px 12px 12px;
  line-height: 1.6;
}
.accordion-body ::v-deep(p) { margin-bottom: 1em; }
</style>
