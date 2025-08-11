<template>
  <div class="service-offers-page">
    <div class="page-header">
      <div class="container">
        <h1>Ofertas de {{ serviceName }}</h1>
        <p>Explore todos os nossos pacotes, hotéis e experiências disponíveis.</p>
      </div>
    </div>

    <div class="filter-bar" v-if="pageData && pageData.services">
      <div class="container filter-container">
        <router-link to="/ofertas/todos" class="filter-btn" exact-active-class="active">Todos</router-link>
        <router-link 
          v-for="service in pageData.services" 
          :key="service.id" 
          :to="`/ofertas/servico/${service.slug}`" 
          class="filter-btn"
          active-class="active"
        >
          <i :class="service.icon_class" aria-hidden="true"></i>
          <span class="filter-name">{{ service.name }}</span>
        </router-link>
      </div>
    </div>

    <div class="container page-content">
      <div v-if="loading" class="loading-spinner"><p>A carregar ofertas...</p></div>
      <div v-if="!loading && offers.length > 0" class="offer-grid">
        <OfferCard 
          v-for="offer in offers" 
          :key="offer.id" 
          :offer="offer" 
          :backend-url="backendUrl"
        />
      </div>
      <div v-if="!loading && offers.length === 0" class="no-offers-message">
        <p>Nenhuma oferta encontrada para esta categoria no momento.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import OfferCard from '../components/OfferCard.vue';
import { BACKEND_URL } from '../config';

export default {
  name: 'ServiceOffersView',
  components: { OfferCard },
  props: {
    pageData: Object,
  },
  data() {
    return {
      offers: [],
      loading: true,
      backendUrl: BACKEND_URL,
    };
  },
  computed: {
    serviceName() {
      const slug = this.$route.params.slug;
      if (!this.pageData || !this.pageData.services) return '...';
      const service = this.pageData.services.find(s => s.slug === slug);
      return service ? service.name : 'Todas as Ofertas';
    }
  },
  watch: {
    '$route.params.slug': {
      immediate: true,
      handler() {
        this.fetchOffers();
      }
    }
  },
  methods: {
    async fetchOffers() {
      this.loading = true;
      const slug = this.$route.params.slug || 'todos';
      const url = `${this.backendUrl}/api/v1/offers/servico/${slug}/`;

      try {
        const response = await axios.get(url);
        this.offers = response.data;
      } catch (error) {
        console.error("Erro ao buscar ofertas do serviço:", error);
        this.offers = [];
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.page-header {
  padding: 50px 0;
  background-color: #003366;
  color: #fff;
  text-align: center;
}
.page-header h1 { font-size: 2.8rem; }

/* Filtro agora rola junto com a página */
.filter-bar {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  position: relative; /* antes era sticky */
  top: auto;
  z-index: 1;
}

.filter-container {
  display: flex;
  gap: 10px;
  padding: 12px 20px;
  align-items: center;
  overflow-x: auto;
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.filter-container::-webkit-scrollbar { display: none; }

.filter-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  padding: 8px 16px;
  border-radius: 50px;
  background: #f5f7fa;
  color: #333;
  text-decoration: none;
  border: 1px solid #e6e6e6;
  font-weight: 500;
  transition: all .2s ease;
}
.filter-btn:hover { transform: translateY(-2px); background: #eef2f7; }
.filter-btn.active {
  background: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
}

.page-content { padding: 50px 20px; }
.loading-spinner, .no-offers-message { text-align: center; padding: 40px 0; color: #666; }

.offer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  align-items: stretch;
}

@media (min-width: 1200px) {
  .offer-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
