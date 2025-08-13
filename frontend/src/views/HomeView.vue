<template>
  <div v-if="pageData">
    <section class="banner-carousel-section" v-if="pageData.banners && pageData.banners.length > 0">
      <Carousel :autoplay="getAutoplaySpeed(pageData.site_configuration.banner_autoplay_speed)" :wrap-around="true">
        <Slide v-for="banner in pageData.banners" :key="banner.id">
          <a :href="banner.link_url || '#'" target="_blank" rel="noopener noreferrer" class="carousel__item">
            <img class="banner-img" :src="`${backendUrl}${banner.image}`" :alt="banner.title">
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
        <div class="booking-form-container" :style="{ height: formContainerHeight }">
          <form @submit.prevent="handleSearchSubmit" v-if="pageData.services && pageData.services.length > 0" ref="formContent">
            <div v-for="service in pageData.services" :key="`form-${service.slug}`">
              <transition name="fade">
                <div v-if="activeTab === service.slug" class="form-panel">
                  <div v-if="activeTab === 'hospedagens'" class="dynamic-form-grid">
                    <div class="form-group destination-group">
                      <label>Cidade, hotel ou destino</label>
                      <input type="text" placeholder="Ex: Rio de Janeiro" v-model="formData.destination">
                    </div>
                    <div class="form-group date-group">
                      <label>Entrada</label>
                      <input type="date" v-model="formData.checkin">
                    </div>
                    <div class="form-group date-group">
                      <label>Saída</label>
                      <input type="date" v-model="formData.checkout">
                    </div>
                    <div class="form-group guests-group">
                      <label>Quartos e Hóspedes</label>
                      <button type="button" class="custom-input-btn" @click="isRoomSelectorOpen = !isRoomSelectorOpen">
                        {{ roomsDisplayText }}
                      </button>
                      <div v-if="isRoomSelectorOpen" class="room-selector-popup">
                        <div v-for="(room, index) in rooms" :key="index" class="room-item">
                          <div class="room-header">
                            <strong>Quarto {{ index + 1 }}</strong>
                            <button type="button" class="remove-room-btn" v-if="rooms.length > 1" @click="removeRoom(index)">Remover</button>
                          </div>
                          <div class="guest-controls">
                            <label>Adultos <span>+18 anos</span></label>
                            <div>
                              <button type="button" @click="room.adults > 1 ? room.adults-- : null" class="stepper-btn">-</button>
                              <span>{{ room.adults }}</span>
                              <button type="button" @click="room.adults++" class="stepper-btn">+</button>
                            </div>
                          </div>
                          <div class="guest-controls">
                            <label>Crianças <span>0-17 anos</span></label>
                            <div>
                              <button type="button" @click="room.children > 0 ? room.children-- : null" class="stepper-btn">-</button>
                              <span>{{ room.children }}</span>
                              <button type="button" @click="room.children++" class="stepper-btn">+</button>
                            </div>
                          </div>
                        </div>
                        <div class="popup-actions">
                          <button type="button" class="add-room-btn" @click="addRoom">Adicionar quarto</button>
                          <button type="button" class="apply-btn" @click="isRoomSelectorOpen = false">Aplicar</button>
                        </div>
                      </div>
                    </div>
                    <div class="form-group button-group">
                      <button type="submit" class="search-button" aria-label="Buscar"><i class="fa-solid fa-magnifying-glass"></i></button>
                    </div>
                  </div>

                  <div v-else class="dynamic-form-grid">
                    <div v-for="(field, index) in service.form_fields" :key="index" class="form-group">
                      <label :for="`${service.slug}-${field.name}`">{{ field.label }}</label>
                      <input :type="field.type" :id="`${service.slug}-${field.name}`" :placeholder="field.placeholder || ''" v-model="formData[field.name]">
                    </div>
                    <div class="form-group button-group">
                      <button type="submit" class="search-button" aria-label="Buscar"><i class="fa-solid fa-magnifying-glass"></i></button>
                    </div>
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
                <OfferCard :offer="offer" :backendUrl="backendUrl" />
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
import OfferCard from '../components/OfferCard.vue';

export default {
  name: 'HomeView',
  components: { Carousel, Slide, Pagination, Navigation, OfferCard },
  props: { pageData: Object, backendUrl: String },
  data() {
    return {
      activeTab: null,
      isRoomSelectorOpen: false,
      rooms: [{ adults: 2, children: 0 }],
      newsletterEmail: '',
      carouselSettings: { itemsToShow: 1.2, snapAlign: 'start', breakpoints: { 600: { itemsToShow: 2.2 }, 900: { itemsToShow: 3.2 }, 1200: { itemsToShow: 4 } } },
      formData: {},
      formContainerHeight: 'auto',
    };
  },
  watch: {
    activeTab() {
      this.formData = {};
      this.updateFormContainerHeight();
    },
    pageData: {
      immediate: true,
      handler(newData) {
        if (newData?.services?.length > 0 && !this.activeTab) {
          this.activeTab = newData.services[0].slug;
        }
        this.updateFormContainerHeight();
      }
    }
  },
  computed: {
    roomsDisplayText() {
      const totalAdults = this.rooms.reduce((acc, room) => acc + room.adults, 0);
      const totalChildren = this.rooms.reduce((acc, room) => acc + room.children, 0);
      const roomCount = this.rooms.length;
      let text = `${totalAdults} Adulto${totalAdults > 1 ? 's' : ''}`;
      if (totalChildren > 0) {
        text += `, ${totalChildren} Criança${totalChildren > 1 ? 's' : ''}`;
      }
      text += ` - ${roomCount} Quarto${roomCount > 1 ? 's' : ''}`;
      return text;
    },
    heroStyle() {
      const config = this.pageData?.site_configuration;
      if (config?.hero_background_image) {
        return { backgroundImage: `linear-gradient(rgba(0,0,0,0.4),rgba(0,0,0,0.4)),url(${this.backendUrl}${config.hero_background_image})` };
      }
      return { backgroundColor: config?.hero_background_color || '#333' };
    },
    servicesWithOffers() {
      return this.pageData?.services?.filter(s => s.offers && s.offers.length > 0) || [];
    },
    newsletterStyle() {
      const config = this.pageData?.site_configuration;
      if (config?.newsletter_background_image) {
        return {
          backgroundImage: `url(${this.backendUrl}${config.newsletter_background_image})`,
          backgroundSize: 'contain',
          backgroundRepeat: 'no-repeat',
          backgroundColor: '#f4f5f7' 
        };
      }
      return { backgroundColor: config?.newsletter_background_color || '#212529' };
    }
  },
  methods: {
    // ===== AJUSTE PONTUAL E PRECISO =====
    // Este método agora encontra o painel ativo e mede a altura *dele*,
    // garantindo o tamanho correto e a transição suave.
    updateFormContainerHeight() {
      this.$nextTick(() => {
        const formWrapper = this.$refs.formContent;
        if (formWrapper) {
          // Procura pelo painel que está de fato visível na tela
          const activePanel = formWrapper.querySelector('.form-panel');
          if (activePanel) {
            // Mede a altura do painel ativo, e não do container geral
            const formHeight = activePanel.scrollHeight;
            this.formContainerHeight = `${formHeight}px`;
          }
        }
      });
    },
    addRoom() { this.rooms.push({ adults: 1, children: 0 }); },
    removeRoom(index) { this.rooms.splice(index, 1); },
    handleSearchSubmit() {
      const serviceSlug = this.activeTab;
      const queryParams = new URLSearchParams();
      
      for (const key in this.formData) {
        if (this.formData[key]) {
          queryParams.append(key, this.formData[key]);
        }
      }
      
      if (serviceSlug === 'hospedagens') {
        queryParams.append('rooms', JSON.stringify(this.rooms));
      }
      
      const searchPath = `/ofertas/servico/${serviceSlug}?${queryParams.toString()}`;
      this.$router.push(searchPath);
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
.banner-carousel-section .carousel__item {
  line-height: 0;
  max-height: 350px;
  overflow: hidden;
  background-color: #f0f2f5;
}
.banner-carousel-section .carousel__item .banner-img {
  width: 100%;
  height: 350px;
  object-fit: contain;
  display: block;
}

@media (max-width: 600px) { .banner-carousel-section .carousel__item { max-height: 220px; } .banner-carousel-section .carousel__item .banner-img { height: 220px; } }
.services-bar { padding: 15px 0; border-bottom: 1px solid #eee; background-color: #fff; font-family: 'Poppins', sans-serif; }
.services-bar .container { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; }
.services-bar button { background: none; border: none; cursor: pointer; padding: 10px 15px; font-size: 1rem; font-family: inherit; display: flex; align-items: center; gap: 8px; transition: color 0.3s, border-color 0.3s; border-bottom: 3px solid transparent; }
.services-bar button.active { color: var(--primary-color); border-bottom-color: var(--primary-color); }
.hero-section { background-size: cover; background-position: center; padding: 60px 0; }

.booking-form-container {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: height 0.35s ease-in-out;
  overflow: hidden;
}

.dynamic-form-grid { display: flex; flex-wrap: wrap; gap: 15px; align-items: flex-end; }
.form-group { flex: 1 1 auto; display: flex; flex-direction: column; min-width: 140px; }
.form-group.destination-group { flex-grow: 2; min-width: 250px; }
.form-group.guests-group { min-width: 220px; position: relative; }
.form-group label { margin-bottom: 8px; font-weight: bold; font-size: 0.9rem; }
.form-group input, .form-group .custom-input-btn { height: 48px; width: 100%; padding: 0 15px; border: 1px solid #ccc; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
.custom-input-btn { text-align: left; background-color: #fff; cursor: pointer; display: flex; align-items: center; }
.form-group.button-group { flex-grow: 0; flex-shrink: 0; min-width: auto; }
.search-button { background-color: var(--primary-color); color: #fff; border: none; height: 48px; width: 50px; border-radius: 8px; cursor: pointer; font-size: 1.5rem; display: flex; justify-content: center; align-items: center; }
.room-selector-popup { position: absolute; top: 100%; left: 0; background: #fff; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.15); padding: 20px; z-index: 100; width: 320px; margin-top: 5px; }
.room-item { margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #eee; }
.room-item:last-child { border-bottom: none; margin-bottom: 0; }
.room-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.remove-room-btn { background: none; border: none; color: #e74c3c; cursor: pointer; font-size: 0.8rem; }
.guest-controls { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.guest-controls label span { display: block; font-size: 0.75rem; color: #777; }
.guest-controls div { display: flex; align-items: center; gap: 10px; }
.stepper-btn { background: #f0f0f0; border: 1px solid #ccc; width: 30px; height: 30px; border-radius: 50%; cursor: pointer; font-weight: bold; }
.popup-actions { display: flex; gap: 10px; margin-top: 15px; }
.add-room-btn, .apply-btn { width: 100%; padding: 10px; border-radius: 4px; border: 1px solid var(--primary-color); cursor: pointer; font-weight: bold; }
.add-room-btn { background: #fff; color: var(--primary-color); }
.apply-btn { background: var(--primary-color); color: #fff; }
.offer-section { padding: 60px 0; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.section-title { font-size: 2.2rem; font-weight: 700; }
.view-all-btn { font-weight: bold; }
.carousel__slide { padding: 10px; display: flex; flex-direction: column; }
.carousel__item { height: 100%; width: 100%; }

.newsletter-section {
  padding: 60px 0;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  position: relative;
  color: #fff;
  text-align: center;
}

.newsletter-overlay { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: rgba(0,0,0,0.0); }
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