<template>
  <div class="about-us-page" v-if="pageData">
    <section class="page-header" :style="headerStyle">
      <div class="header-overlay"></div>
      <div class="container header-content">
        <h1>{{ pageData.site_configuration.about_page_title || 'Conheça a Nossa História' }}</h1>
        <p>{{ pageData.site_configuration.about_page_subtitle || 'Transformamos sonhos em viagens inesquecíveis.' }}</p>
      </div>
    </section>

    <section class="content-section">
      <div class="container">
        <div class="history-content" v-html="pageData.site_configuration.about_us_history"></div>
      </div>
    </section>

    <section class="values-section">
      <div class="container">
        <div class="values-grid">
          <div class="value-card">
            <i class="fa-solid fa-rocket"></i>
            <h3>Nossa Missão</h3>
            <p>{{ pageData.site_configuration.about_us_mission }}</p>
          </div>
          <div class="value-card">
            <i class="fa-solid fa-eye"></i>
            <h3>Nossa Visão</h3>
            <p>{{ pageData.site_configuration.about_us_vision }}</p>
          </div>
          <div class="value-card">
            <i class="fa-solid fa-heart"></i>
            <h3>Nossos Valores</h3>
            <ul>
              <li v-for="(value, index) in pageData.site_configuration.about_us_values.split('\n')" :key="index">{{ value }}</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- SEÇÃO DA EQUIPE AJUSTADA -->
    <section class="team-section" v-if="teamMembers && teamMembers.length > 0">
      <div class="container">
        <h2 class="section-title">Conheça a equipe que transforma viagens em histórias.</h2>
        <div class="team-grid">
          <div v-for="member in teamMembers" :key="member.id" class="team-card">
            <img :src="getMediaUrl(member.photo)" :alt="member.name">
            <h4>{{ member.name }}</h4>
            <p class="role">{{ member.role }}</p>
            <p class="bio">"{{ member.bio }}"</p>
          </div>
        </div>
      </div>
    </section>

    <section class="stats-section">
      <div class="container">
        <div class="stat-item">
          <strong>{{ pageData.site_configuration.stat_years }}</strong>
          <span>Anos no Mercado</span>
        </div>
        <div class="stat-item">
          <strong>{{ pageData.site_configuration.stat_destinations }}</strong>
          <span>Destinos Atendidos</span>
        </div>
        <div class="stat-item">
          <strong>{{ pageData.site_configuration.stat_clients }}</strong>
          <span>Clientes Felizes</span>
        </div>
      </div>
    </section>

    <section class="cta-section">
      <div class="container">
        <h2>Vamos planear a sua próxima viagem?</h2>
        <router-link to="/contato" class="cta-button">Fale com um especialista</router-link>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL, getMediaUrl } from '../config';

export default {
  name: 'AboutUsView',
  props: { pageData: Object },
  data() {
    return {
      teamMembers: [],
      backendUrl: BACKEND_URL,
    };
  },
  computed: {
    headerStyle() {
      const config = this.pageData?.site_configuration;
      if (!config) return { backgroundColor: '#003366' };
      if (config.about_us_header_image) return { backgroundImage: `url(${this.getMediaUrl(config.about_us_header_image)})` };
      if (config.page_header_bg_color) return { backgroundColor: config.page_header_bg_color };
      return { backgroundColor: '#003366' };
    }
  },
  methods: {
    getMediaUrl,
    async fetchTeamMembers() {
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/company-info/team/`);
        this.teamMembers = response.data;
      } catch (error) {
        console.error("Erro ao buscar membros da equipa:", error);
      }
    }
  },
  created() {
    this.fetchTeamMembers();
  }
}
</script>

<style scoped>
/* CABEÇALHO */
.page-header {
  position: relative;
  height: 40vh;
  min-height: 300px;
  background-size: cover;
  background-position: center;
  color: #fff;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.header-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.7), rgba(0,0,0,0.3));
}
.header-content { position: relative; z-index: 2; }
.header-content h1 { font-size: 2.4rem; font-weight: 700; margin-bottom: 0.3rem; }
.header-content p { font-size: 1.1rem; margin: 0; }

/* HISTÓRIA */
.content-section { padding: 40px 0; }
.history-content { max-width: 720px; margin: 0 auto; line-height: 1.6; font-size: 1rem; }

/* VALORES */
.values-section { background-color: #f8f9fa; padding: 40px 0; }
.values-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; }
.value-card { background: #fff; padding: 25px; border-radius: 8px; text-align: center; }
.value-card i { font-size: 2.2rem; color: var(--primary-color); margin-bottom: 12px; }
.value-card h3 { margin-bottom: 8px; font-weight: 600; }
.value-card ul { list-style: none; padding: 0; margin: 0; font-size: 0.95rem; line-height: 1.4; }

/* EQUIPE AJUSTADA */
.team-section { padding: 40px 0; }
.section-title { text-align: center; font-size: 1.8rem; margin-bottom: 30px; }
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); /* largura mínima e máxima do card */
  gap: 5px; /* espaçamento entre cards */
  justify-items: center; /* centraliza horizontalmente */
}
.team-card { text-align: center; max-width: 200px; }
.team-card img {
  width: 110px; /* tamanho da foto */
  height: 110px; /* mantém proporção */
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 12px;
}
.team-card h4 { margin-bottom: 4px; font-size: 1rem; }
.team-card .role { color: #666; font-size: 0.85rem; margin-bottom: 8px; }
.team-card .bio { font-style: italic; font-size: 0.85rem; margin: 0; }

/* ESTATÍSTICAS */
.stats-section { background-color: var(--primary-color); color: #fff; padding: 40px 0; }
.stats-section .container { display: flex; justify-content: space-around; text-align: center; flex-wrap: wrap; gap: 25px; }
.stat-item strong { display: block; font-size: 2rem; font-weight: 700; }
.stat-item span { display: block; font-size: 1rem; margin-top: 5px; }

/* CTA FINAL */
.cta-section { padding: 40px 0; text-align: center; }
.cta-button {
  display: inline-block;
  padding: 14px 28px;
  background-color: var(--primary-color);
  color: #fff;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}
.cta-button:hover { background-color: #004a99; }
</style>
