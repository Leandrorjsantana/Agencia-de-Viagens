<template>
  <div class="experiences-page">
    <div class="page-header" :style="headerStyle">
      <div class="container">
        <h1 v-if="pageData">{{ pageData.site_configuration.experiences_page_title }}</h1>
        <p v-if="pageData">{{ pageData.site_configuration.experiences_page_subtitle }}</p>
        <router-link v-if="isLoggedIn" to="/area-cliente/avaliacoes/nova" class="cta-button">Deixe sua avaliação</router-link>
      </div>
    </div>

    <!-- NOVA SECÇÃO DE ESTATÍSTICAS -->
    <section class="stats-section" v-if="stats">
      <div class="container">
        <div class="stat-item">
          <strong>{{ stats.average_rating }} / 5.0</strong>
          <span>Média Geral</span>
        </div>
        <div class="stat-item">
          <strong>{{ stats.total_reviews }}</strong>
          <span>Avaliações</span>
        </div>
        <div class="stat-item">
          <strong>{{ stats.satisfied_percentage }}%</strong>
          <span>Clientes Satisfeitos</span>
        </div>
      </div>
    </section>

    <div class="container page-content">
      <!-- NOVA SECÇÃO DE FILTROS -->
      <div class="filters-container">
        <div class="search-filter">
          <input type="text" v-model="filters.search" placeholder="Pesquisar por destino ou palavra-chave...">
        </div>
        <div class="rating-filter">
          <select v-model="filters.rating">
            <option value="">Todas as Notas</option>
            <option value="5">Apenas 5 Estrelas</option>
            <option value="4">4 Estrelas ou mais</option>
            <option value="3">3 Estrelas ou mais</option>
          </select>
        </div>
      </div>

      <div v-if="loading" class="loading-spinner"><p>A carregar experiências...</p></div>
      <div v-if="!loading && reviews.length > 0" class="reviews-grid">
        <ReviewCard 
          v-for="review in reviews" 
          :key="review.id" 
          :review="review" 
        />
      </div>
      <div v-if="!loading && reviews.length === 0" class="no-reviews-message">
        <p>Nenhuma avaliação encontrada para os critérios selecionados.</p>
      </div>
    </div>

    <section class="final-cta-section">
      <div class="container">
        <h2>Pronto para viver a sua própria experiência inesquecível?</h2>
        <router-link to="/ofertas/servico/todos" class="cta-button">Ver todos os pacotes</router-link>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL } from '../config';
import ReviewCard from '../components/ReviewCard.vue';

export default {
  name: 'ExperiencesView',
  components: { ReviewCard },
  props: { pageData: Object },
  data() {
    return {
      reviews: [],
      stats: null,
      loading: true,
      isLoggedIn: false,
      filters: {
        search: '',
        rating: '',
      }
    };
  },
  computed: {
    headerStyle() {
      const config = this.pageData?.site_configuration;
      return { backgroundColor: config?.page_header_bg_color || '#003366' };
    }
  },
  watch: {
    filters: {
      handler() {
        this.fetchReviews();
      },
      deep: true
    }
  },
  methods: {
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('accessToken');
    },
    async fetchReviews() {
      this.loading = true;
      try {
        const params = new URLSearchParams();
        if (this.filters.search) params.append('search', this.filters.search);
        if (this.filters.rating) params.append('rating__gte', this.filters.rating);

        const response = await axios.get(`${BACKEND_URL}/api/v1/reviews/list/`, { params });
        this.reviews = response.data;
      } catch (error) {
        console.error("Erro ao buscar avaliações:", error);
      } finally {
        this.loading = false;
      }
    },
    async fetchStats() {
      try {
        const response = await axios.get(`${BACKEND_URL}/api/v1/reviews/stats/`);
        this.stats = response.data;
      } catch (error) {
        console.error("Erro ao buscar estatísticas:", error);
      }
    }
  },
  created() {
    this.checkLoginStatus();
    this.fetchReviews();
    this.fetchStats();
  }
}
</script>

<style scoped>
.page-header { padding: 60px 0; color: #fff; text-align: center; }
.page-header h1 { font-size: 2.8rem; }
.page-header p { font-size: 1.2rem; margin-top: 10px; }
.cta-button { display: inline-block; margin-top: 25px; padding: 12px 25px; background-color: #fff; color: var(--primary-color); border-radius: 50px; text-decoration: none; font-weight: bold; }

.stats-section { background-color: #f8f9fa; padding: 30px 0; border-bottom: 1px solid #e9ecef; }
.stats-section .container { display: flex; justify-content: space-around; text-align: center; }
.stat-item strong { display: block; font-size: 2rem; font-weight: 700; }

.filters-container { display: flex; gap: 15px; margin-bottom: 40px; justify-content: center; }
.search-filter input { 
  width: 250px; /* tamanho ajustável */
  padding: 8px 12px; 
  font-size: 0.85rem;
  border-radius: 25px; /* bordas arredondadas */
  border: 1px solid #ccc;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
  transition: all 0.2s ease;
}
.search-filter input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.rating-filter select { 
  width: 150px; /* tamanho ajustável */
  padding: 8px 12px; 
  font-size: 0.85rem;
  border-radius: 25px; 
  border: 1px solid #ccc;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  transition: all 0.2s ease;
  background-color: #fff;
}
.rating-filter select:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.page-content { padding: 50px 20px; }
.reviews-grid { display: grid; grid-template-columns: 1fr; gap: 30px; align-items: stretch; }
@media (min-width: 768px) { .reviews-grid { grid-template-columns: 1fr 1fr; } }
@media (min-width: 1200px) { .reviews-grid { grid-template-columns: 1fr 1fr 1fr; } }

.final-cta-section { background-color: #f8f9fa; padding: 60px 20px; text-align: center; }
.final-cta-section h2 { font-size: 2rem; margin-bottom: 25px; }
.final-cta-section .cta-button { background-color: var(--primary-color); color: #fff; }
</style>
