<template>
  <div class="reservations-page">
    <div class="page-header">
      <h1>Minhas Reservas</h1>
      <p>Aqui você pode ver o histórico e o status de todas as suas compras.</p>
    </div>

    <div v-if="loading" class="loading-spinner">
      <p>Buscando suas reservas...</p>
    </div>

    <div v-if="!loading && reservations.length > 0" class="reservations-list">
      <div v-for="reservation in reservations" :key="reservation.id" class="reservation-card">
        <div class="card-header">
          <div class="header-info">
            <h3 v-if="reservation.offer">{{ reservation.offer.title }}</h3>
            <span>Código: {{ reservation.reservation_code }}</span>
          </div>
          <div class="status-badge" :class="`status-${reservation.status.toLowerCase()}`">
            {{ reservation.status_display }}
          </div>
        </div>

        <div class="card-body">
          <div class="offer-image">
            <img
              v-if="reservation.offer && reservation.offer.image"
              :src="getMediaUrl(reservation.offer.image)"
              alt="Imagem da Oferta"
            />
            <div v-else class="image-placeholder"></div>
          </div>
          <div class="reservation-details">
            <p v-if="reservation.offer"><strong>Destino:</strong> {{ reservation.offer.subtitle }}</p>
            <p><strong>Data da Viagem:</strong> {{ formatDate(reservation.start_date) }} a {{ formatDate(reservation.end_date) }}</p>
            <p><strong>Valor Total:</strong> R$ {{ reservation.total_price }}</p>
          </div>
        </div>

        <div class="card-footer">
          <div class="documents-section">
            <h4>Documentos da Viagem:</h4>
            <ul v-if="reservation.documents.length > 0">
              <li v-for="doc in reservation.documents" :key="doc.id">
                <a
                  :href="getMediaUrl(doc.file)"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <i class="fa-solid fa-file-arrow-down"></i>
                  {{ doc.description }}
                </a>
              </li>
            </ul>
            <p v-else>Nenhum documento disponível.</p>
          </div>
          <!-- NOVO: Botão de Upload que só aparece se o status for 'PENDING' -->
          <div class="upload-action" v-if="reservation.status === 'PENDING'">
            <button @click="openUploadModal(reservation.id)" class="upload-button">
              <i class="fa-solid fa-cloud-arrow-up"></i>
              Enviar Comprovativo
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && reservations.length === 0" class="no-reservations">
      <i class="fa-solid fa-folder-open"></i>
      <h3>Nenhuma reserva encontrada</h3>
      <router-link to="/" class="explore-button">Explorar Destinos</router-link>
    </div>
  </div>

  <!-- NOVO: Modal de Upload de Documentos -->
  <div v-if="isUploadModalOpen" class="modal-overlay" @click.self="closeUploadModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Enviar Comprovativo</h2>
        <button @click="closeUploadModal" class="close-button">&times;</button>
      </div>
      <form @submit.prevent="handleUploadSubmit" class="modal-form">
        <div class="form-field">
          <label for="doc-description">Descrição do Arquivo</label>
          <input type="text" id="doc-description" v-model="uploadDescription" placeholder="Ex: Comprovativo PIX" required>
        </div>
        <div class="form-field">
          <label for="doc-file">Selecione o Arquivo</label>
          <input type="file" id="doc-file" @change="handleFileChange" required>
        </div>
        <div v-if="uploadError" class="error-message">{{ uploadError }}</div>
        <div class="modal-actions">
          <button type="button" @click="closeUploadModal" class="cancel-button">Cancelar</button>
          <button type="submit" class="submit-button" :disabled="isUploading">
            {{ isUploading ? 'Enviando...' : 'Enviar' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BACKEND_URL, getMediaUrl } from "../../config";

export default {
  name: "ReservationsView",
  data() {
    return {
      reservations: [],
      loading: true,
      errorMessage: null,
      backendUrl: BACKEND_URL,
      // Novos estados para controlar o modal de upload
      isUploadModalOpen: false,
      currentReservationId: null,
      uploadDescription: '',
      uploadFile: null,
      isUploading: false,
      uploadError: null,
    };
  },
  async created() {
    await this.fetchReservations();
  },
  methods: {
    getMediaUrl, // Sua função importada para montar URLs corretas

    getAuthHeaders() {
      const token = localStorage.getItem("accessToken");
      if (!token) return {};
      return { Authorization: `Bearer ${token}` };
    },

    async fetchReservations() {
      this.loading = true;
      this.errorMessage = null;
      try {
        const response = await axios.get(
          `${this.backendUrl}/api/v1/reservations/my-reservations/`,
          { headers: this.getAuthHeaders() }
        );
        this.reservations = response.data;
      } catch (error) {
        this.errorMessage = "Não foi possível carregar suas reservas.";
        console.error("Erro ao buscar reservas:", error);
      } finally {
        this.loading = false;
      }
    },

    formatDate(dateString) {
      const date = new Date(`${dateString}T00:00:00`);
      const options = { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" };
      return date.toLocaleDateString("pt-BR", options);
    },

    // --- NOVOS MÉTODOS PARA O MODAL ---
    openUploadModal(reservationId) {
      this.currentReservationId = reservationId;
      this.isUploadModalOpen = true;
      this.uploadError = null;
    },
    closeUploadModal() {
      this.isUploadModalOpen = false;
      this.uploadDescription = '';
      this.uploadFile = null;
    },
    handleFileChange(event) {
      this.uploadFile = event.target.files[0];
    },
    async handleUploadSubmit() {
      if (!this.uploadFile) {
        this.uploadError = "Por favor, selecione um ficheiro.";
        return;
      }
      this.isUploading = true;
      this.uploadError = null;

      const formData = new FormData();
      formData.append('description', this.uploadDescription);
      formData.append('file', this.uploadFile);

      try {
        const headers = this.getAuthHeaders();
        headers['Content-Type'] = 'multipart/form-data';

        await axios.post(
          `${this.backendUrl}/api/v1/reservations/${this.currentReservationId}/upload-document/`,
          formData,
          { headers: headers }
        );
        
        alert("Comprovativo enviado com sucesso!");
        this.closeUploadModal();
        await this.fetchReservations();

      } catch (error) {
        this.uploadError = "Ocorreu um erro ao enviar o ficheiro. Tente novamente.";
        console.error("Erro no upload:", error);
      } finally {
        this.isUploading = false;
      }
    }
  },
};
</script>

<style scoped>
.page-header { margin-bottom: 40px; }
.page-header h1 { font-size: 2.2rem; }
.reservations-list { display: grid; gap: 30px; }
.reservation-card { background: #fff; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.07); overflow: hidden; }
.card-header { display: flex; justify-content: space-between; align-items: center; padding: 20px; background-color: #f8f9fa; border-bottom: 1px solid #e9ecef; }
.header-info h3 { margin: 0; font-size: 1.3rem; }
.header-info span { font-size: 0.9rem; color: #6c757d; }
.status-badge { padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; color: #fff; }
.status-pending { background-color: #ffc107; color: #333; }
.status-confirmed { background-color: #198754; }
.status-canceled { background-color: #dc3545; }
.status-completed { background-color: #6c757d; }
.card-body { display: flex; gap: 20px; padding: 20px; }
.offer-image img, .image-placeholder { width: 150px; height: 100px; object-fit: cover; border-radius: 8px; background-color: #eee; }
.reservation-details p { margin: 0 0 10px 0; }
.card-footer { padding: 20px; background-color: #f8f9fa; border-top: 1px solid #e9ecef; display: flex; justify-content: space-between; align-items: center; }
.documents-section h4 { margin: 0 0 10px 0; }
.documents-section ul { list-style: none; padding: 0; margin: 0; }
.documents-section li a { color: var(--primary-color); text-decoration: none; font-weight: 500; }
.documents-section li a i { margin-right: 8px; }
.upload-button { background-color: var(--primary-color); color: #fff; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; cursor: pointer; display: flex; align-items: center; gap: 8px; }
.no-reservations { text-align: center; padding: 50px; background: #fff; border-radius: 12px; }
.no-reservations i { font-size: 3rem; color: #ccc; }
.explore-button { display: inline-block; margin-top: 20px; padding: 12px 25px; background-color: var(--primary-color); color: #fff; border-radius: 50px; text-decoration: none; font-weight: bold; }

/* Estilos do Modal */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.6); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: #fff; padding: 30px; border-radius: 12px; width: 100%; max-width: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
.modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee; padding-bottom: 15px; margin-bottom: 20px; }
.modal-header h2 { margin: 0; }
.close-button { background: none; border: none; font-size: 1.5rem; cursor: pointer; }
.modal-form .form-field { margin-bottom: 20px; }
.modal-form label { display: block; margin-bottom: 8px; font-weight: 500; }
.modal-form input { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 5px; }
.modal-actions { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; }
.cancel-button, .submit-button { padding: 10px 20px; border-radius: 5px; border: none; font-weight: bold; cursor: pointer; }
.cancel-button { background-color: #f0f0f0; }
.submit-button { background-color: var(--primary-color); color: #fff; }
.submit-button:disabled { background-color: #ccc; }
</style>