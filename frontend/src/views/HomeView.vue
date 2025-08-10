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
            <h2>{{ service.section_headline || 'Ofertas de ' + service.name }}</h2>
            <router-link :to="`/ofertas/servico/${service.slug}`" class="view-all-btn">Ver todas as ofertas</router-link>
          </div>
          <Carousel v-bind="carouselSettings" :autoplay="getAutoplaySpeed(pageData.site_configuration.offer_carousel_speed)">
            <Slide v-for="offer in service.offers" :key="offer.id">
              <div class="carousel__item">
                <div class="offer-card">
                  <div class="offer-image-container"><img :src="`${backendUrl}${offer.image}`" :alt="offer.subtitle"></div>
                  <div class="card-content">
                    <div class="card-content-top">
                      <span v-if="offer.promo_tag" class="promo-tag">{{ offer.promo_tag }}</span>
                      <span class="package-details-card">{{ offer.title }}</span>
                      <h3 class="offer-title-card">{{ offer.subtitle }}</h3>
                    </div>
                    <div class="card-content-bottom">
                      <div class="price-section">
                         <span class="price-value">R$ {{ offer.price }}</span>
                      </div>
                      <router-link :to="`/ofertas/${offer.slug}`" class="details-button">Reservar</router-link>
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
    }
  }
};
</script>

<style scoped>
/* Importa o CSS do Carrossel */
@import 'vue3-carousel/dist/carousel.css';

/* --- CORREÇÃO DO BANNER --- */
.banner-carousel-section .carousel__item {
  height: auto; /* A altura se ajusta ao conteúdo */
  width: 100%;
  color: white;
}
.banner-carousel-section .carousel__item img {
  width: 100%;
  height: auto; /* A altura se ajusta para manter a proporção */
  display: block; /* Remove espaço extra abaixo da imagem */
  max-height: 70vh; /* Limita a altura máxima em telas grandes */
  object-fit: cover; /* Garante que a imagem cubra a área se necessário */
}
/* ------------------------- */

.carousel__pagination-button--active::after { background-color: var(--primary-color) !important; }
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
.room-selector-popup { position: absolute; top: 105%; left: 0; background: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 15px; z-index: 100; min-width: 300px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
.room-item { margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #eee; }
.room-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.guest-controls { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
.guest-controls label span { font-size: 0.8rem; color: #777; }
.stepper-btn { background-color: #f0f0f0; border: 1px solid #ccc; width: 30px; height: 30px; border-radius: 50%; cursor: pointer; font-weight: bold; }
.popup-actions { display: flex; justify-content: space-between; margin-top: 15px; }
.add-room-btn, .apply-btn, .remove-room-btn { border: none; background: none; cursor: pointer; font-weight: bold; }
.add-room-btn { color: var(--primary-color); }
.apply-btn { background-color: var(--primary-color); color: #fff; padding: 8px 15px; border-radius: 5px; }
.offer-section { padding: 60px 0; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.section-header h2 { font-size: 2.2rem; font-weight: 700; }
.carousel__item { padding: 0 10px; }
.offer-card { background: #fff; border-radius: 8px; overflow: hidden; text-align: left; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
.offer-image-container img { width: 100%; height: 200px; object-fit: cover; }
.card-content { padding: 20px; }
.card-content-bottom { display: flex; justify-content: space-between; align-items: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid #f0f0f0; }
.price-value { font-size: 1.5rem; font-weight: bold; color: var(--primary-color); }
.details-button { background-color: var(--primary-color); color: #fff; padding: 8px 16px; border-radius: 5px; font-weight: 500; }
.newsletter-section { padding: 80px 0; background-size: cover; background-position: center; position: relative; color: #fff; text-align: center; }
.newsletter-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.6); }
.newsletter-content { position: relative; z-index: 2; }
.newsletter-form { margin-top: 20px; display: flex; justify-content: center; gap: 10px; }
.newsletter-form input { padding: 15px; width: 300px; border: none; border-radius: 5px; }
.newsletter-button { padding: 15px 35px; border: none; border-radius: 50px; background-color: var(--primary-color); color: #fff; font-weight: bold; font-size: 1rem; cursor: pointer; transition: transform 0.2s ease, box-shadow 0.2s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
.newsletter-button:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.3); }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
