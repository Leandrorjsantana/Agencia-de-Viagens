<template>
  <div class="contact-page">
    <div class="page-header" v-if="pageData?.site_configuration">
      <div class="container">
        <h1>{{ pageData.site_configuration.contact_page_title }}</h1>
        <p>{{ pageData.site_configuration.contact_page_subtitle }}</p>
      </div>
    </div>

    <div class="container page-content">
      <div class="contact-grid">
        <!-- Coluna da Esquerda: Informações e Mapa -->
        <div class="contact-info-wrapper">
          <div class="info-block">
            <h3>Nossas Informações</h3>
            <div class="info-item" v-if="fullAddress">
              <i class="fa-solid fa-location-dot"></i>
              <span>{{ fullAddress }}</span>
            </div>
            <div class="info-item" v-if="pageData.site_configuration.public_whatsapp">
              <i class="fa-brands fa-whatsapp"></i>
              <a :href="`https://wa.me/${pageData.site_configuration.public_whatsapp}`" target="_blank">{{ pageData.site_configuration.public_whatsapp }}</a>
            </div>
            <div class="info-item" v-if="pageData.site_configuration.public_email">
              <i class="fa-solid fa-envelope"></i>
              <a :href="`mailto:${pageData.site_configuration.public_email}`">{{ pageData.site_configuration.public_email }}</a>
            </div>
            <div class="info-item" v-if="pageData.site_configuration.opening_hours">
              <i class="fa-solid fa-clock"></i>
              <pre>{{ pageData.site_configuration.opening_hours }}</pre>
            </div>
          </div>
          <div class="map-block" v-if="pageData.site_configuration.google_maps_embed_url">
            <iframe
              :src="pageData.site_configuration.google_maps_embed_url"
              width="100%"
              height="300"
              style="border:0;"
              allowfullscreen=""
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>
        </div>

        <!-- Coluna da Direita: Formulário de Contato -->
        <div class="contact-form-wrapper">
          <h3>Envie-nos uma Mensagem</h3>
          <form @submit.prevent="handleContactSubmit">
            <div class="form-field">
              <label for="contact-name">Nome Completo</label>
              <input type="text" id="contact-name" v-model="contactForm.full_name" required>
            </div>
            <div class="form-grid">
              <div class="form-field">
                <label for="contact-email">E-mail</label>
                <input type="email" id="contact-email" v-model="contactForm.email" required>
              </div>
              <div class="form-field">
                <!-- CORREÇÃO: O rótulo agora não diz mais "Opcional" -->
                <label for="contact-phone">Telefone</label>
                <!-- CORREÇÃO: O campo agora é 'required' -->
                <input type="tel" id="contact-phone" v-model="contactForm.phone" required>
              </div>
            </div>
            <div class="form-field">
              <label for="contact-subject">Assunto</label>
              <select id="contact-subject" v-model="contactForm.subject" required>
                <option disabled value="">Selecione um assunto</option>
                <option v-for="subject in contactSubjects" :key="subject" :value="subject">
                  {{ subject }}
                </option>
              </select>
            </div>
            <div class="form-field">
              <label for="contact-message">Mensagem</label>
              <textarea id="contact-message" v-model="contactForm.message" rows="5" required></textarea>
            </div>
            
            <div v-if="formError" class="error-message">{{ formError }}</div>
            <div v-if="formSuccess" class="success-message">Mensagem enviada com sucesso! Obrigado.</div>

            <button type="submit" class="submit-button" :disabled="isSubmitting">
              {{ isSubmitting ? 'A enviar...' : 'Enviar Mensagem' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL } from '../config';

export default {
  name: 'ContactView',
  props: {
    pageData: Object,
  },
  data() {
    return {
      backendUrl: BACKEND_URL,
      isSubmitting: false,
      formError: null,
      formSuccess: false,
      contactForm: {
        full_name: '',
        email: '',
        phone: '',
        subject: '',
        message: '',
      },
    };
  },
  computed: {
    contactSubjects() {
      const subjectsText = this.pageData?.site_configuration?.contact_form_subjects || '';
      return subjectsText.split('\n').map(s => s.trim()).filter(Boolean);
    },
    fullAddress() {
      if (!this.pageData?.site_configuration) return '';
      const config = this.pageData.site_configuration;
      const parts = [
        config.address_street,
        config.address_neighborhood,
        config.address_city,
        config.address_state,
        config.address_cep,
      ].filter(Boolean);
      return parts.join(', ');
    }
  },
  methods: {
    async handleContactSubmit() {
      this.isSubmitting = true;
      this.formError = null;
      this.formSuccess = false;

      try {
        await axios.post(`${this.backendUrl}/api/v1/contacts/submit/`, this.contactForm);
        this.formSuccess = true;
        this.contactForm = {
          full_name: '',
          email: '',
          phone: '',
          subject: '',
          message: '',
        };
      } catch (error) {
        this.formError = "Ocorreu um erro ao enviar a sua mensagem. Tente novamente.";
        console.error("Erro ao enviar mensagem de contato:", error);
      } finally {
        this.isSubmitting = false;
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

.page-content {
  padding: 60px 20px;
}
.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 50px;
}
.info-block {
  margin-bottom: 30px;
}
.info-block h3 {
  font-size: 1.5rem;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--primary-color);
}
.info-item {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 1.1rem;
}
.info-item i {
  color: var(--primary-color);
  width: 20px;
}
.info-item pre {
  font-family: inherit;
  margin: 0;
  white-space: pre-wrap;
}
.map-block iframe {
  border-radius: 8px;
}
.contact-form-wrapper {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.08);
}
.contact-form-wrapper h3 {
  font-size: 1.5rem;
  margin-top: 0;
  margin-bottom: 25px;
}
.form-field { margin-bottom: 20px; }
.form-field label { display: block; font-weight: 500; margin-bottom: 8px; }
.form-field input, .form-field textarea, .form-field select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  font-family: inherit;
  box-sizing: border-box;
}
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.submit-button {
  width: 100%;
  padding: 15px;
  font-size: 1.1rem;
  font-weight: bold;
  color: #fff;
  background-color: var(--primary-color);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: opacity 0.3s;
}
.submit-button:disabled { background-color: #ccc; }
.error-message { background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
.success-message { background-color: #d4edda; color: #155724; padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 20px; }
</style>