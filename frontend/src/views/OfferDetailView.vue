<template>
  <div class="offer-detail-page">
    <div v-if="loading" class="loading-container">
      <p>A carregar detalhes da oferta...</p>
    </div>

    <div v-if="!loading && offer" class="container">
      <div class="offer-grid">
        <div class="offer-main-content">
          <div class="offer-gallery">
            <img :src="getMediaUrl(offer.image)" :alt="offer.title" class="main-image">
          </div>
          <div class="offer-description">
            <h2>Sobre o Pacote</h2>
            <p>{{ offer.subtitle }}</p>
            
            <div v-if="offer.long_description" v-html="offer.long_description" class="long-description"></div>

            <div class="offer-includes" v-if="offer.details">
              <h3>O que está incluído:</h3>
              <ul>
                <li v-for="(item, index) in offer.details.split('\n')" :key="index">
                  <i class="fa-solid fa-check"></i>{{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <aside class="offer-sidebar">
          <div class="price-card">
            <span class="package-details-card">{{ offer.subtitle }}</span>
            <h1 class="offer-title">{{ offer.title }}</h1>
            
            <div class="hotel-info" v-if="offer.hotel_name">
              <span v-if="offer.hotel_rating" class="hotel-rating">{{ offer.hotel_rating }}</span>
              <span class="hotel-name">{{ offer.hotel_name }}</span>
            </div>

            <div class="price-section">
              <div class="savings-highlight" v-if="offer.original_price && offer.original_price > offer.price">
                Economize R$ {{ formatPrice(offer.original_price - offer.price) }}
              </div>
              <div class="price-original-line" v-if="offer.original_price">
                <span class="original-price">R$ {{ formatPrice(offer.original_price) }}</span>
              </div>
              <span class="price-label">{{ offer.price_per_person ? 'Preço por pessoa' : '' }}</span>
              <div class="price-final-line">
                <span class="price-currency">R$</span>
                <span class="price-value">{{ formatPrice(offer.price) }}</span>
              </div>
              <span class="taxes-info">{{ offer.taxes_included ? 'Taxas e impostos inclusos' : 'Taxas e impostos não inclusos' }}</span>
            </div>
            
            <button @click="handleReserveClick" class="reserve-button">Quero Reservar</button>
          </div>
        </aside>
      </div>
    </div>

    <div v-if="error" class="error-message">
      <p>Não foi possível encontrar a oferta solicitada.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL, getMediaUrl } from '../config';

export default {
  name: 'OfferDetailView',
  data() {
    return {
      offer: null,
      loading: true,
      error: false,
      backendUrl: BACKEND_URL,
    };
  },
  async created() {
    await this.fetchOfferDetails();
  },
  methods: {
    getMediaUrl,
    async fetchOfferDetails() {
      this.loading = true;
      this.error = false;
      const slug = this.$route.params.slug;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/offers/${slug}/`);
        this.offer = response.data;
      } catch (err) {
        this.error = true;
        console.error("Erro ao buscar detalhes da oferta:", err);
      } finally {
        this.loading = false;
      }
    },
    formatPrice(value) {
      const number = parseFloat(value);
      if (isNaN(number)) return value;
      return new Intl.NumberFormat('pt-BR').format(number);
    },
    handleReserveClick() {
      const token = localStorage.getItem('accessToken');
      if (token) {
        alert('Utilizador está logado! Próximo passo: formulário de reserva pré-preenchido.');
      } else {
        this.$router.push({ name: 'login', query: { redirect: this.$route.fullPath } });
      }
    }
  }
};
</script>

<style scoped>
.offer-detail-page { padding: 40px 0; }
.container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }
.offer-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 40px; }
.main-image { width: 100%; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
.offer-description { margin-top: 30px; }
.offer-description h2 { font-size: 1.8rem; margin-bottom: 15px; }
.long-description { margin-top: 20px; line-height: 1.7; }
.offer-includes { margin-top: 20px; }
.offer-includes h3 { font-size: 1.2rem; }
.offer-includes ul { list-style: none; padding: 0; }
.offer-includes li { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.offer-includes .fa-check { color: #198754; }
.price-card { background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); position: sticky; top: 120px; }
.package-details-card { font-size: 0.8rem; color: #666; text-transform: uppercase; }
.offer-title { font-size: 1.8rem; margin: 5px 0 15px 0; }
.hotel-info { display: flex; align-items: center; gap: 8px; margin-bottom: 15px; font-size: 0.9rem; }
.hotel-rating { background-color: #003366; color: #fff; font-weight: bold; padding: 3px 8px; border-radius: 4px; }
.price-section { margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; }
.savings-highlight { background-color: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; display: inline-block; margin-bottom: 8px; }
.price-original-line { font-size: 0.9rem; color: #777; text-decoration: line-through; }
.price-label { font-size: 0.8rem; color: #777; }
.price-final-line { display: flex; align-items: baseline; gap: 4px; }
.price-currency { font-size: 1.2rem; font-weight: 500; }
.price-value { font-size: 2.5rem; font-weight: 700; color: var(--primary-color); }
.taxes-info { font-size: 0.7rem; color: #777; display: block; margin-top: 2px; }
.reserve-button { width: 100%; margin-top: 25px; padding: 16px; font-size: 1.2rem; font-weight: bold; border-radius: 8px; background-color: var(--primary-color); color: #fff; border: none; cursor: pointer; transition: all 0.2s ease-in-out; }
.reserve-button:hover { transform: translateY(-3px); box-shadow: 0 8px 25px rgba(13, 110, 253, 0.4); }
</style>