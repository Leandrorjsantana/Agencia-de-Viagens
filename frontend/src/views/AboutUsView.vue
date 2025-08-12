<template>
  <div class="about-us-page" v-if="pageData">
    <!-- 1. Cabeçalho Inspirador -->
    <section class="page-header" :style="headerStyle">
      <div class="header-overlay"></div>
      <div class="container header-content">
        <h1>Conheça a Rio Mundo Viagens</h1>
        <p>Transformamos sonhos em viagens inesquecíveis.</p>
      </div>
    </section>

    <!-- 2. História da Agência -->
    <section class="content-section">
      <div class="container">
        <div class="history-content" v-html="pageData.site_configuration.about_us_history"></div>
      </div>
    </section>

    <!-- 3. Missão, Visão e Valores -->
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

    <!-- 5. Equipa -->
    <section class="team-section" v-if="teamMembers && teamMembers.length > 0">
      <div class="container">
        <h2 class="section-title">Nossa Equipa</h2>
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

    <!-- 6. Credibilidade -->
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

    <!-- 7. Chamado à Ação Final -->
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
      const img = this.pageData?.site_configuration?.about_us_header_image;
      if (img) {
        return { backgroundImage: `url(${this.getMediaUrl(img)})` };
      }
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
/* Estilos para uma página "Quem Somos" moderna e inspiradora */
.page-header {
  position: relative;
  height: 50vh;
  min-height: 350px;
  background-size: cover;
  background-position: center;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.header-overlay {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(to top, rgba(0,0,0,0.7), rgba(0,0,0,0.3));
}
.header-content {
  position: relative;
  z-index: 2;
}
.header-content h1 { font-size: 3rem; font-weight: 700; }
.header-content p { font-size: 1.2rem; }

.content-section { padding: 60px 0; }
.history-content { max-width: 800px; margin: 0 auto; line-height: 1.8; font-size: 1.1rem; }
.history-content ::v-deep(h2) { text-align: center; margin-bottom: 30px; }

.values-section { background-color: #f8f9fa; padding: 60px 0; }
.values-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }
.value-card { background: #fff; padding: 30px; border-radius: 8px; text-align: center; }
.value-card i { font-size: 2.5rem; color: var(--primary-color); margin-bottom: 15px; }
.value-card h3 { margin-bottom: 10px; }
.value-card ul { list-style: none; padding: 0; }

.team-section { padding: 60px 0; }
.section-title { text-align: center; font-size: 2.2rem; margin-bottom: 40px; }
.team-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; }
.team-card { text-align: center; }
.team-card img { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 15px; }
.team-card h4 { margin-bottom: 5px; }
.team-card .role { color: #777; }
.team-card .bio { font-style: italic; }

.stats-section { background-color: var(--primary-color); color: #fff; padding: 50px 0; }
.stats-section .container { display: flex; justify-content: space-around; text-align: center; }
.stat-item strong { display: block; font-size: 2.5rem; font-weight: 700; }

.cta-section { padding: 60px 0; text-align: center; }
.cta-button { display: inline-block; padding: 15px 30px; background-color: var(--primary-color); color: #fff; border-radius: 50px; text-decoration: none; font-weight: bold; }
</style>