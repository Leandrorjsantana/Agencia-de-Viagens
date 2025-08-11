<template>
  <div v-if="pageData">
    <section class="banner-carousel-section" v-if="pageData.banners && pageData.banners.length > 0">
      <Carousel :autoplay="getAutoplaySpeed(pageData.site_configuration.banner_autoplay_speed)" :wrap-around="true">
        <Slide v-for="banner in pageData.banners" :key="banner.id">
          <a :href="banner.link_url || '#'" target="_blank" rel="noopener noreferrer" class="carousel__item">
            <img :src="`${backendUrl}${banner.image}`" :alt="banner.title">
          </a>
        </Slide>
        <template #addons>
          <Navigation />
          <Pagination />
        </template>
      </Carousel>
    </section>

    <div class="services-bar" v-if="pageData.services && pageData.services.length > 0">
      <div class="container">
        <button v-for="service in pageData.services" :key="service.slug" @click="activeTab = service.slug" :class="{ active: activeTab === service.slug }">
          <i :class="service.icon_class"></i>
          <span>{{ service.name }}</span>
        </button>
      </div>
    </div>

    <main class="hero-section" :style="heroStyle">
      <div class="container">
        <div class="booking-form-container">
          <form @submit.prevent="handleSearchSubmit" v-if="pageData.services && pageData.services.length > 0">
            <div v-for="service in pageData.services" :key="`form-${service.slug}`">
              <transition name="fade">
                <div v-if="activeTab === service.slug" class="form-panel">
                  <div v-if="activeTab === 'hospedagens'" class="dynamic-form-grid">
                    <div class="form-group destination-group"><label>Cidade, hotel ou destino</label><input type="text" placeholder="Ex: Rio de Janeiro" v-model="formData.destination"></div>
                    <div class="form-group date-group"><label>Entrada</label><input type="date" v-model="formData.checkin"></div>
                    <div class="form-group date-group"><label>Saída</label><input type="date" v-model="formData.checkout"></div>
                    <div class="form-group guests-group"><label>Quartos e Hóspedes</label><button type="button" class="custom-input-btn" @click="isRoomSelectorOpen = !isRoomSelectorOpen">{{ roomsDisplayText }}</button><div v-if="isRoomSelectorOpen" class="room-selector-popup"><div v-for="(room, index) in rooms" :key="index" class="room-item"><div class="room-header"><strong>Quarto {{ index + 1 }}</strong><button type="button" class="remove-room-btn" v-if="rooms.length > 1" @click="removeRoom(index)">Remover</button></div><div class="guest-controls"><label>Adultos <span>+18 anos</span></label><div><button type="button" @click="room.adults > 1 ? room.adults-- : null" class="stepper-btn">-</button><span>{{ room.adults }}</span><button type="button" @click="room.adults++" class="stepper-btn">+</button></div></div><div class="guest-controls"><label>Crianças <span>0-17 anos</span></label><div><button type="button" @click="room.children > 0 ? room.children-- : null" class="stepper-btn">-</button><span>{{ room.children }}</span><button type="button" @click="room.children++" class="stepper-btn">+</button></div></div></div><div class="popup-actions"><button type="button" class="add-room-btn" @click="addRoom">Adicionar quarto</button><button type="button" class="apply-btn" @click="isRoomSelectorOpen = false">Aplicar</button></div></div></div>
                    <div class="form-group button-group"><button type="submit" class="search-button" aria-label="Buscar"><i class="fa-solid fa-magnifying-glass"></i></button></div>
                  </div>
                  <div v-else class="dynamic-form-grid">
                    <div v-for="(field, index) in service.form_fields" :key="index" class="form-group"><label :for="`${service.slug}-${field.name}`">{{ field.label }}</label><input :type="field.type" :id="`${service.slug}-${field.name}`" :placeholder="field.placeholder || ''" v-model="formData[field.name]"></div>
                    <div class="form-group button-group"><button type="submit" class="search-button" aria-label="Buscar"><i class="fa-solid fa-magnifying-glass"></i></button></div>
                  </div>
                </div>
              </transition>
            </div>
          </form>
        </div>
      </div>
    </main>

    <div class="content-sections">
      <section v-for="service in servicesWithOffers" :key="`section-${service.slug}`" class="offer-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">{{ service.section_headline || 'Ofertas de ' + service.name }}</h2>
            <router-link :to="`/ofertas/servico/${service.slug}`" class="view-all-btn">Ver todas as ofertas</router-link>
          </div>
          <Carousel v-bind="carouselSettings" :wrap-around="service.offers.length > 4" :autoplay="getAutoplaySpeed(pageData.site_configuration.offer_carousel_speed)">
            <Slide v-for="offer in service.offers" :key="offer.id">
              <div class="carousel__item">
                <div class="offer-card">
                  <div class="offer-image-container">
                    <img :src="`${backendUrl}${offer.image}`" :alt="offer.subtitle">
                    <div class="duration-on-image" v-if="offer.duration_days">
                      <span>{{ offer.duration_days }} DIAS / {{ offer.duration_nights }} NOITES</span>
                    </div>
                  </div>
                  <div class="card-content">
                    <div class="card-content-top">
                      <span v-if="offer.promo_tag" class="promo-tag">{{ offer.promo_tag }}</span>
                      <!-- CORREÇÃO FINAL: Invertendo a ordem e o conteúdo das variáveis -->
                      <span class="package-details-card">{{ offer.subtitle }}</span>
                      <h3 class="offer-title-card">{{ offer.title }}</h3>
                      <div class="hotel-info" v-if="offer.hotel_name">
                        <span v-if="offer.hotel_rating" class="hotel-rating">{{ offer.hotel_rating }}</span>
                        <span class="hotel-name">{{ offer.hotel_name }}</span>
                      </div>
                      <p class="origin-card" v-if="offer.origin"><i class="fa-solid fa-plane-departure"></i> Saindo de {{ offer.origin }}</p>
                      <div class="offer-includes" v-if="offer.details">
                        <p v-for="(item, index) in offer.details.split('\n')" :key="index">
                          <i class="fa-solid fa-check"></i>{{ item }}
                        </p>
                      </div>
                    </div>
                    <div class="card-content-bottom">
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
                      <router-link :to="`/ofertas/${offer.slug}`" class="details-button" :class="{ highlighted: offer.highlight_button }">Reservar</router-link>
                    </div>
                  </div>
                </div>
              </div>
            </Slide>
            <template #addons><Navigation /></template>
          </Carousel>
        </div>
      </section>
    </div>

    <section class="newsletter-section" :style="newsletterStyle">
      <div class="newsletter-overlay"></div>
      <div class="container newsletter-content">
        <h2>{{ pageData.site_configuration.newsletter_headline }}</h2>
        <p>{{ pageData.site_configuration.newsletter_subheadline }}</p>
        <form class="newsletter-form" @submit.prevent="handleNewsletterSubmit">
          <input type="email" placeholder="Digite seu melhor e-mail" v-model="newsletterEmail" required>
          <button type="submit" class="newsletter-button">{{ pageData.site_configuration.newsletter_button_text }}</button>
        </form>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import { Carousel, Navigation, Pagination, Slide } from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';

export default {
  name: 'HomeView',
  components: { Carousel, Slide, Pagination, Navigation },
  props: { pageData: Object, backendUrl: String },
  data() {
    return {
      activeTab: null,
      isRoomSelectorOpen: false,
      rooms: [{ adults: 2, children: 0 }],
      newsletterEmail: '',
      carouselSettings: { itemsToShow: 1.2, snapAlign: 'start', breakpoints: { 600: { itemsToShow: 2.2 }, 900: { itemsToShow: 3.2 }, 1200: { itemsToShow: 4 } } },
      formData: {}
    };
  },
  watch: {
    activeTab() { this.formData = {}; },
    pageData: {
      immediate: true,
      handler(newData) {
        if (newData?.services?.length > 0) { this.activeTab = newData.services[0].slug; }
      }
    }
  },
  computed: {
    roomsDisplayText() { const totalAdults = this.rooms.reduce((acc, room) => acc + room.adults, 0); const totalChildren = this.rooms.reduce((acc, room) => acc + room.children, 0); const roomCount = this.rooms.length; let text = `${totalAdults} Adulto${totalAdults > 1 ? 's' : ''}`; if (totalChildren > 0) { text += `, ${totalChildren} Criança${totalChildren > 1 ? 's' : ''}`; } text += ` - ${roomCount} Quarto${roomCount > 1 ? 's' : ''}`; return text; },
    heroStyle() { const config = this.pageData?.site_configuration; if (config?.hero_background_image) { return { backgroundImage: `linear-gradient(rgba(0,0,0,0.4),rgba(0,0,0,0.4)),url(${this.backendUrl}${config.hero_background_image})` }; } return { backgroundColor: config?.hero_background_color || '#333' }; },
    servicesWithOffers() { return this.pageData?.services?.filter(s => s.offers && s.offers.length > 0) || []; },
    newsletterStyle() { const config = this.pageData?.site_configuration; if (config?.newsletter_background_image) { return { backgroundImage: `url(${this.backendUrl}${config.newsletter_background_image})` }; } return { backgroundColor: config?.newsletter_background_color || '#212529' }; }
  },
  methods: {
    addRoom() { this.rooms.push({ adults: 1, children: 0 }); },
    removeRoom(index) { this.rooms.splice(index, 1); },
    handleSearchSubmit() {
      const serviceSlug = this.activeTab;
      const queryParams = new URLSearchParams();
      for (const key in this.formData) {
        if (this.formData[key]) { queryParams.append(key, this.formData[key]); }
      }
      if (serviceSlug === 'hospedagens') {
        queryParams.append('rooms', JSON.stringify(this.rooms));
      }
      this.$router.push(`/ofertas/servico/${serviceSlug}?${queryParams.toString()}`);
    },
    async handleNewsletterSubmit() {
      try {
        const response = await axios.post(`${this.backendUrl}/api/v1/subscribers/subscribe/`, { email: this.newsletterEmail });
        if (response.status === 201) {
          alert(this.pageData.site_configuration.newsletter_success_message || "Inscrição realizada com sucesso!");
          this.newsletterEmail = '';
        }
      } catch (error) {
        alert("Ocorreu um erro ao se inscrever.");
      }
    },
    getAutoplaySpeed(speed) {
      const speedMs = Number(speed);
      return !isNaN(speedMs) && speedMs > 0 ? speedMs : 0;
    },
    formatPrice(value) {
      const number = parseFloat(value);
      if (isNaN(number)) return value;
      return new Intl.NumberFormat('pt-BR').format(number);
    }
  }
};
</script>

<style scoped>
@import 'vue3-carousel/dist/carousel.css';

.banner-carousel-section .carousel__slide { height: auto; }
.banner-carousel-section .carousel__item { line-height: 0; max-height: 400px; overflow: hidden; }
.banner-carousel-section .carousel__item img { width: 100%; height: 100%; object-fit: cover; display: block; }
.services-bar { padding: 15px 0; border-bottom: 1px solid #eee; background-color: #fff; }
.services-bar .container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }
.services-bar button { background: none; border: none; cursor: pointer; padding: 10px 15px; font-size: 1rem; display: flex; align-items: center; gap: 8px; transition: color 0.3s, border-color 0.3s; border-bottom: 3px solid transparent; }
.services-bar button.active { color: var(--primary-color); border-bottom-color: var(--primary-color); }
.hero-section { background-size: cover; background-position: center; padding: 60px 0; }
.booking-form-container { background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
.dynamic-form-grid { display: flex; flex-wrap: wrap; gap: 15px; align-items: flex-end; }
.form-group { flex: 1 1 auto; display: flex; flex-direction: column; min-width: 140px; }
.form-group.destination-group { flex-grow: 2; min-width: 250px; }
.form-group.guests-group { min-width: 220px; }
.form-group label { margin-bottom: 8px; font-weight: bold; font-size: 0.9rem; }
.form-group input, .form-group .custom-input-btn { height: 48px; width: 100%; padding: 0 15px; border: 1px solid #ccc; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
.custom-input-btn { text-align: left; background-color: #fff; cursor: pointer; display: flex; align-items: center; }
.form-group.button-group { flex-grow: 0; flex-shrink: 0; min-width: auto; }
.search-button { background-color: var(--primary-color); color: #fff; border: none; height: 48px; width: 50px; border-radius: 8px; cursor: pointer; font-size: 1.5rem; display: flex; justify-content: center; align-items: center; }
.offer-section { padding: 60px 0; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.section-title { font-size: 2.2rem; font-weight: 700; }
.view-all-btn { font-weight: bold; }
.carousel__slide { padding: 10px; display: flex; flex-direction: column; }
.carousel__item { height: 100%; width: 100%; }
.offer-card { background: #fff; border-radius: 12px; box-shadow: 0 6px 25px rgba(0,0,0,0.08); display: flex; flex-direction: column; text-align: left; width: 100%; height: 100%; transition: box-shadow 0.3s, transform 0.3s; }
.offer-card:hover { transform: translateY(-5px); box-shadow: 0 12px 35px rgba(0,0,0,0.12); }
.card-content { padding: 20px; display: flex; flex-direction: column; flex-grow: 1; }
.card-content-top { flex-grow: 1; }
.card-content-bottom { margin-top: 15px; padding-top: 15px; border-top: 1px solid #f0f0f0; }
.offer-image-container { position: relative; }
.offer-image-container img { width: 100%; height: 200px; object-fit: cover; }
.duration-on-image { position: absolute; bottom: 10px; left: 10px; background-color: rgba(0,0,0,0.6); color: #fff; padding: 5px 10px; border-radius: 5px; font-size: 0.8rem; font-weight: bold; }
.promo-tag { display: inline-block; margin-bottom: 12px; background-color: #e6f7ff; color: #096dd9; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; }
/* CORREÇÃO FINAL: Invertendo os estilos dos títulos */
.package-details-card { display: block; font-size: 0.8rem; color: #666; text-transform: uppercase; font-weight: 500; margin-bottom: 5px; }
.offer-title-card { font-size: 1.4rem; font-weight: 700; color: #333; margin: 0 0 10px 0; line-height: 1.3; }
.hotel-info { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; font-size: 0.9rem; }
.hotel-rating { background-color: #003366; color: #fff; font-weight: bold; padding: 3px 8px; border-radius: 4px; }
.origin-card { font-size: 0.9rem; color: #777; margin: 8px 0; display: flex; align-items: center; gap: 5px; }
.offer-includes { font-size: 0.9rem; color: #555; line-height: 1.6; }
.offer-includes p { margin: 0 0 2px 0; display: flex; align-items: center; }
.offer-includes .fa-check { color: #198754; margin-right: 8px; }
.price-section { text-align: right; }
.savings-highlight { background-color: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; display: inline-block; margin-bottom: 8px; }
.price-original-line { font-size: 0.9rem; color: #777; }
.original-price { text-decoration: line-through; }
.price-label { font-size: 0.8rem; color: #777; display: block; margin-top: -5px; }
.price-final-line { display: flex; align-items: baseline; justify-content: flex-end; gap: 2px; }
.price-currency { font-size: 1.1rem; font-weight: 500; color: #333; }
.price-value { font-size: 2.2rem; font-weight: 700; color: var(--primary-color); }
.taxes-info { font-size: 0.7rem; color: #777; display: block; margin-top: 2px; }
.details-button { width: 100%; margin-top: 15px; padding: 14px; font-size: 1.1rem; font-weight: bold; border-radius: 8px; background-color: var(--primary-color); color: #fff; border: none; cursor: pointer; text-decoration: none; display: inline-block; text-align: center; transition: all 0.2s ease-in-out; }
.details-button.highlighted { background-color: #ffc107; color: #000; }
.details-button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 25px rgba(13, 110, 253, 0.4); }
.newsletter-section { padding: 60px 0; background-size: cover; background-position: center; position: relative; color: #fff; text-align: center; }
.newsletter-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.6); }
.newsletter-content { position: relative; z-index: 2; }
.newsletter-content h2 { font-size: 2rem; margin-bottom: 10px; }
.newsletter-content p { font-size: 1.1rem; margin-bottom: 25px; }
.newsletter-form { display: flex; justify-content: center; max-width: 500px; margin: 0 auto; }
.newsletter-form input { flex-grow: 1; padding: 15px; border: 1px solid #ccc; border-radius: 50px 0 0 50px; font-size: 1rem; outline: none; border-right: none; }
.newsletter-button { padding: 15px 30px; border: none; background-color: var(--primary-color); color: white; font-size: 1rem; font-weight: bold; border-radius: 0 50px 50px 0; cursor: pointer; transition: opacity 0.2s; }
.newsletter-button:hover { opacity: 0.9; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>