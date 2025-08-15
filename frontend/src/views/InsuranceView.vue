<template>
  <div class="insurance-page">
    <!-- Cabeçalho -->
    <section class="page-header" :style="headerStyle">
      <div class="container">
        <h1>Viaje tranquilo com nosso Seguro Viagem</h1>
        <p>Proteção completa em qualquer destino.</p>
        <a href="#plans" class="cta-button">Faça sua cotação agora</a>
      </div>
    </section>

    <div v-if="loading" class="loading-spinner">
      <p>Carregando informações...</p>
    </div>

    <div v-if="!loading && pageContent">
      <!-- Benefícios -->
      <section class="benefits-section">
        <div class="container">
          <h2 class="section-title">Por que escolher nosso Seguro Viagem?</h2>
          <div class="benefits-grid">
            <div v-for="benefit in pageContent.benefits" :key="benefit.title" class="benefit-card">
              <i :class="benefit.icon_class"></i>
              <h3>{{ benefit.title }}</h3>
              <p>{{ benefit.description }}</p>
              <div v-if="benefit.long_description" class="long-description" v-html="benefit.long_description"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- Planos -->
      <section id="plans" class="plans-section">
        <div class="container">
          <h2 class="section-title">Nossos Planos</h2>
          <div class="plans-grid">
            <div v-for="plan in pageContent.plans" :key="plan.name" class="plan-card" :class="{ popular: plan.is_popular }">
              <div v-if="plan.is_popular" class="popular-badge">Mais Popular</div>
              <h3>{{ plan.name }}</h3>
              <p class="price-info">{{ plan.price_info }}</p>
              <div class="features" v-html="plan.features"></div>
              <a :href="whatsappLink" target="_blank" class="cta-button">Contratar Agora</a>
            </div>
          </div>
        </div>
      </section>

      <!-- FAQ -->
      <section class="faq-section">
        <div class="container">
          <h2 class="section-title">Perguntas Frequentes</h2>
          <div class="faq-accordion">
            <div v-for="(faq, index) in pageContent.faqs" :key="index" class="faq-item">
              <button @click="toggleFaq(index)" class="faq-question">
                <span>{{ faq.question }}</span>
                <i class="fa-solid" :class="openFaq === index ? 'fa-minus' : 'fa-plus'"></i>
              </button>
              <div v-if="openFaq === index" class="faq-answer">
                <p>{{ faq.answer }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Selos -->
      <section class="seals-section" v-if="pageContent.seals?.length">
        <div class="container">
          <h3 class="seals-title">Nossos Parceiros e Selos de Confiança</h3>
          <div class="seals-grid">
            <div v-for="seal in pageContent.seals" :key="seal.name" class="seal-item">
              <img :src="getMediaUrl(seal.logo)" :alt="seal.name">
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL, getMediaUrl } from '../config';

export default {
  name: 'InsuranceView',
  props: { pageData: Object },
  data() {
    return { pageContent: null, loading: true, openFaq: null };
  },
  computed: {
    headerStyle() {
      const config = this.pageData?.site_configuration;
      return { backgroundColor: config?.page_header_bg_color || '#003366' };
    },
    whatsappLink() {
      const config = this.pageData?.site_configuration;
      const phone = config?.public_whatsapp || '';
      const message = "Olá! Gostaria de fazer uma cotação para o Seguro Viagem.";
      return `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
    }
  },
  methods: {
    getMediaUrl,
    async fetchInsuranceData() {
      this.loading = true;
      try {
        const { data } = await axios.get(`${BACKEND_URL}/api/v1/insurance/page-data/`);
        this.pageContent = data;
      } catch (error) {
        console.error("Erro ao buscar dados do seguro viagem:", error);
      } finally {
        this.loading = false;
      }
    },
    toggleFaq(index) {
      this.openFaq = this.openFaq === index ? null : index;
    }
  },
  created() {
    this.fetchInsuranceData();
  }
};
</script>

<style scoped>
/* Cabeçalho */
.page-header {
  padding: 40px 0;
  color: #fff;
  text-align: center;
}
.page-header h1 {
  font-size: 2.2rem;
  margin-bottom: 8px;
}
.page-header p {
  font-size: 1rem;
}

/* Botões com vida e animação */
.cta-button {
  display: inline-block;
  margin-top: 15px;
  padding: 12px 25px;
  background: linear-gradient(135deg, var(--primary-color), #ff8c00);
  color: #fff;
  border-radius: 30px;
  text-decoration: none;
  font-weight: bold;
  font-size: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
  animation: pulse 2.5s infinite;
}
.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}

/* Seção Títulos */
.section-title {
  text-align: center;
  font-size: 1.8rem;
  margin-bottom: 25px;
}

/* Benefícios */
.benefits-section {
  padding: 40px 0;
  background-color: #f8f9fa;
}
.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 20px;
}
.benefit-card {
  text-align: center;
  padding: 15px;
}
.benefit-card i {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 10px;
}
.long-description {
  margin-top: 10px;
  font-size: 0.9rem;
  color: #555;
  text-align: left;
}

/* Planos */
.plans-section {
  padding: 40px 0;
}
.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}
.plan-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.plan-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}
.plan-card.popular {
  border-color: var(--primary-color);
  border-width: 2px;
}
.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--primary-color);
  color: #fff;
  padding: 3px 10px;
  border-radius: 15px;
  font-size: 0.75rem;
}
.price-info {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 8px 0;
}
.features {
  margin: 15px 0;
}
.features ::v-deep(ul) {
  list-style: none;
  padding: 0;
}
.features ::v-deep(li) {
  margin-bottom: 8px;
}

/* Botão dos planos */
.plan-card .cta-button {
  background: linear-gradient(135deg, var(--primary-color), #ff8c00);
  color: #fff;
  padding: 12px 25px;
  font-size: 1rem;
  border-radius: 30px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
  animation: pulse 2.5s infinite;
}
.plan-card .cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}

/* FAQ com mais vida */
.faq-section {
  padding: 40px 0;
  background-color: #f8f9fa;
}
.faq-accordion {
  max-width: 700px;
  margin: 0 auto;
}
.faq-item {
  border-bottom: 1px solid #ddd;
  transition: all 0.3s ease;
}
.faq-question {
  width: 100%;
  background: var(--primary-color);
  color: #fff;
  border: none;
  text-align: left;
  padding: 15px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  border-radius: 8px;
  transition: background 0.3s ease;
}
.faq-question:hover {
  background: #ff8c00;
}
.faq-answer {
  padding: 10px 15px 15px 15px;
  background: #fff3e6;
  border-radius: 0 0 8px 8px;
  margin-top: 5px;
}

/* Selos */
.seals-section {
  padding: 30px 0;
  text-align: center;
}
.seals-title {
  font-size: 0.95rem;
  color: #6c757d;
  margin-bottom: 15px;
}
.seals-grid {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 25px;
  flex-wrap: wrap;
}
.seal-item img {
  max-height: 45px;
  filter: grayscale(1);
  opacity: 0.7;
}
</style>
