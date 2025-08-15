<template>
  <div class="televendas-page">
    <div class="page-header" :style="headerStyle">
      <div class="container">
        <h1 v-if="pageData">{{ pageData.site_configuration.televendas_page_title }}</h1>
        <p v-if="pageData">{{ pageData.site_configuration.televendas_page_subtitle }}</p>
      </div>
    </div>

    <div class="container page-content">
      <div class="contact-grid">
        <!-- Coluna da Esquerda: Botões de Ação -->
        <div class="contact-actions">
          <div class="action-card" v-if="pageData.site_configuration.televendas_phone">
            <i class="fa-solid fa-phone-volume"></i>
            <h3>Ligue para Nós</h3>
            <p>Fale diretamente com um dos nossos especialistas.</p>
            <a :href="`tel:${pageData.site_configuration.televendas_phone}`" class="action-button phone-btn">
              {{ pageData.site_configuration.televendas_phone }}
            </a>
          </div>
          <div class="action-card" v-if="pageData.site_configuration.public_whatsapp">
            <i class="fa-brands fa-whatsapp"></i>
            <h3>WhatsApp</h3>
            <p>Prefere enviar uma mensagem? Estamos online para o atender.</p>
            <a :href="`https://wa.me/${pageData.site_configuration.public_whatsapp}`" target="_blank" class="action-button whatsapp-btn">
              Iniciar Conversa
            </a>
          </div>
          <div class="info-card" v-if="pageData.site_configuration.opening_hours">
            <i class="fa-solid fa-clock"></i>
            <h4>Horário de Atendimento</h4>
            <pre>{{ pageData.site_configuration.opening_hours }}</pre>
          </div>
        </div>

        <!-- Coluna da Direita: Benefícios -->
        <div class="benefits-section">
          <h3>Por que reservar conosco?</h3>
          <div v-if="pageData.site_configuration.televendas_benefits" v-html="pageData.site_configuration.televendas_benefits" class="benefits-content"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TelevendasView',
  props: {
    pageData: Object,
  },
  computed: {
    headerStyle() {
      const config = this.pageData?.site_configuration;
      if (config && config.page_header_bg_color) {
        return { backgroundColor: config.page_header_bg_color };
      }
      return { backgroundColor: '#003366' }; // Cor de fallback
    }
  }
}
</script>

<style scoped>
.page-header {
  padding: 50px 0;
  color: #fff;
  text-align: center;
}
.page-header h1 { font-size: 2.4rem; margin-bottom: 10px; }
.page-header p { font-size: 1.1rem; margin-top: 0; }

.page-content {
  padding: 40px 20px;
}
.contact-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}
@media (min-width: 992px) {
  .contact-grid {
    grid-template-columns: 1fr 1fr;
    align-items: flex-start;
  }
}

.contact-actions {
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center; /* centraliza os botões */
}
.action-card, .info-card {
  background: #fff;
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 6px 18px rgba(0,0,0,0.08);
  transition: transform 0.2s, box-shadow 0.3s;
  width: 100%;
  max-width: 280px; /* reduz tamanho dos cards */
}
.action-card i {
  font-size: 2rem;
  color: var(--primary-color);
  margin-bottom: 12px;
}
.action-card h3 {
  font-size: 1.2rem;
  margin: 0 0 8px 0;
}
.action-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.18);
}

.action-button {
  display: inline-block;
  width: auto; /* tamanho mais compacto */
  padding: 10px 18px;
  margin-top: 15px;
  border-radius: 8px;
  color: #fff;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
  transition: transform 0.2s, box-shadow 0.3s, background-color 0.3s;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  text-align: center;
}
.action-button:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 20px rgba(0,0,0,0.25);
}

/* Pulsar suave */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}

.action-button.phone-btn {
  background-color: #343a40;
  animation: pulse 3s infinite ease-in-out;
}
.action-button.whatsapp-btn {
  background-color: #25D366;
  animation: pulse 3s infinite ease-in-out 0.5s;
}

.info-card {
  background-color: #f8f9fa;
  box-shadow: none;
  border: 1px solid #e9ecef;
}
.info-card i {
  font-size: 1.5rem;
  color: #6c757d;
  margin-bottom: 10px;
}
.info-card pre {
  font-family: inherit;
  margin: 0;
  white-space: pre-wrap;
  font-size: 1.05rem;
  line-height: 1.5;
}

.benefits-section h3 {
  font-size: 1.6rem;
  margin-bottom: 15px;
}
.benefits-content ::v-deep(ul) {
  list-style: none;
  padding: 0;
}
.benefits-content ::v-deep(li) {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 1.05rem;
  margin-bottom: 12px;
}
.benefits-content ::v-deep(li::before) {
  content: '\f058';
  font-family: 'Font Awesome 6 Free';
  font-weight: 900;
  color: #198754;
  font-size: 1.1rem;
}
</style>
