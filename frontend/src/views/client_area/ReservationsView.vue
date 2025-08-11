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

        <div class="card-footer" v-if="reservation.documents.length > 0">
          <h4>Documentos da Viagem:</h4>
          <ul>
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
        </div>
      </div>
    </div>

    <div v-if="!loading && reservations.length === 0" class="no-reservations">
      <i class="fa-solid fa-folder-open"></i>
      <h3>Nenhuma reserva encontrada</h3>
      <router-link to="/" class="explore-button">Explorar Destinos</router-link>
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
    };
  },
  async created() {
    await this.fetchReservations();
  },
  methods: {
    getMediaUrl, // função importada para montar URLs corretas

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
.card-footer { padding: 20px; background-color: #f8f9fa; border-top: 1px solid #e9ecef; }
.card-footer h4 { margin: 0 0 10px 0; }
.card-footer ul { list-style: none; padding: 0; margin: 0; }
.card-footer li a { color: var(--primary-color); text-decoration: none; font-weight: 500; }
.card-footer li a i { margin-right: 8px; }
.no-reservations { text-align: center; padding: 50px; background: #fff; border-radius: 12px; }
.no-reservations i { font-size: 3rem; color: #ccc; }
.explore-button { display: inline-block; margin-top: 20px; padding: 12px 25px; background-color: var(--primary-color); color: #fff; border-radius: 50px; text-decoration: none; font-weight: bold; }
</style>
