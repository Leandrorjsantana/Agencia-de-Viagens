<template>
  <div class="submit-review-page">
    <div class="page-header">
      <h1>Deixe sua Avaliação</h1>
      <p>Partilhe a sua experiência e ajude outros viajantes a escolherem o seu próximo destino.</p>
    </div>

    <div v-if="loading" class="loading-spinner">
      <p>A carregar as suas viagens concluídas...</p>
    </div>

    <div v-if="!loading && completedReservations.length === 0" class="no-reservations-message">
      <p>Você ainda não tem viagens concluídas para avaliar. Assim que uma viagem for finalizada, ela aparecerá aqui!</p>
    </div>

    <form v-if="!loading && completedReservations.length > 0" @submit.prevent="submitReview" class="review-form">
      <div class="form-field">
        <label for="reservation">Qual viagem você quer avaliar?</label>
        <select id="reservation" v-model="reviewForm.offer" required>
          <option disabled value="">Selecione uma viagem concluída</option>
          <option v-for="res in completedReservations" :key="res.id" :value="res.offer_id">
            {{ res.offer_title }}
          </option>
        </select>
      </div>

      <div class="form-field">
        <label>Qual a sua nota?</label>
        <div class="star-rating">
          <span v-for="n in 5" :key="n" @click="reviewForm.rating = n" class="star">
            <i class="fa-star" :class="n <= reviewForm.rating ? 'fa-solid' : 'fa-regular'"></i>
          </span>
        </div>
      </div>

      <div class="form-field">
        <label for="review-title">Título da sua avaliação</label>
        <input type="text" id="review-title" v-model="reviewForm.title" placeholder="Ex: Uma viagem inesquecível!" required>
      </div>

      <div class="form-field">
        <label for="review-content">A sua mensagem</label>
        <textarea id="review-content" v-model="reviewForm.content" rows="6" placeholder="Conte-nos como foi a sua experiência..." required></textarea>
      </div>
      
      <div class="form-field">
        <label for="review-photo">Envie uma foto da sua viagem (opcional)</label>
        <input type="file" id="review-photo" @change="handleFileChange" accept="image/*">
      </div>

      <div v-if="formError" class="error-message">{{ formError }}</div>

      <button type="submit" class="submit-button" :disabled="isSubmitting">
        {{ isSubmitting ? 'A publicar...' : 'Publicar Avaliação' }}
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL } from '../../config';

export default {
  name: 'SubmitReviewView',
  data() {
    return {
      completedReservations: [],
      loading: true,
      isSubmitting: false,
      formError: null,
      backendUrl: BACKEND_URL,
      reviewForm: {
        offer: '',
        rating: 5,
        title: '',
        content: '',
        photo: null,
      },
    };
  },
  async created() {
    await this.fetchCompletedReservations();
  },
  methods: {
    getAuthHeaders() {
      const token = localStorage.getItem('accessToken');
      if (!token) return {};
      return { 'Authorization': `Bearer ${token}` };
    },
    async fetchCompletedReservations() {
      this.loading = true;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/reservations/for-review/`, {
          headers: this.getAuthHeaders()
        });
        this.completedReservations = response.data;
      } catch (error) {
        console.error("Erro ao buscar reservas para avaliação:", error);
      } finally {
        this.loading = false;
      }
    },
    handleFileChange(event) {
      this.reviewForm.photo = event.target.files[0];
    },
    async submitReview() {
      this.isSubmitting = true;
      this.formError = null;

      const formData = new FormData();
      formData.append('offer', this.reviewForm.offer);
      formData.append('rating', this.reviewForm.rating);
      formData.append('title', this.reviewForm.title);
      formData.append('content', this.reviewForm.content);
      if (this.reviewForm.photo) {
        formData.append('photo', this.reviewForm.photo);
      }

      try {
        const headers = this.getAuthHeaders();
        headers['Content-Type'] = 'multipart/form-data';
        await axios.post(`${this.backendUrl}/api/v1/reviews/my-reviews/`, formData, { headers });
        
        alert('Avaliação enviada com sucesso! Obrigado pela sua contribuição.');
        this.$router.push('/experiencias');

      } catch (error) {
        this.formError = "Ocorreu um erro ao enviar a sua avaliação. Tente novamente.";
        console.error("Erro ao submeter avaliação:", error);
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>

<style scoped>
.page-header {
  text-align: center;
  margin-bottom: 20px; /* Menos espaço */
}
.page-header h1 {
  font-size: 1.6rem; /* Um pouco menor */
  margin-bottom: 5px;
}
.page-header p {
  font-size: 0.95rem;
  color: #555;
}

.review-form {
  background: #fff;
  padding: 20px; /* Reduzi */
  border-radius: 8px;
  max-width: 600px; /* Mais estreito */
  margin: 0 auto;
}

.form-field {
  margin-bottom: 15px; /* Menos espaçamento */
}
.form-field label {
  display: block;
  font-weight: 500;
  margin-bottom: 5px;
  font-size: 0.95rem;
}

.form-field input,
.form-field textarea,
.form-field select {
  width: 100%;
  padding: 10px; /* Reduzi */
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 0.95rem;
  box-sizing: border-box;
}

.star-rating {
  font-size: 1.6rem; /* Menor que antes */
  color: #ffc107;
  cursor: pointer;
}
.star-rating .star {
  margin-right: 4px;
}

.submit-button {
  width: 100%;
  padding: 12px;
  font-size: 1rem; /* Menor */
  font-weight: bold;
  color: #fff;
  background-color: var(--primary-color);
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  padding: 8px; /* Menor */
  border-radius: 5px;
  margin-bottom: 12px;
  font-size: 0.95rem;
}

.no-reservations-message {
  text-align: center;
  padding: 25px; /* Menor */
  background-color: #f8f9fa;
  border-radius: 8px;
  font-size: 0.95rem;
}

.loading-spinner {
  text-align: center;
  padding: 20px;
  font-size: 0.95rem;
  color: #555;
}
</style>

