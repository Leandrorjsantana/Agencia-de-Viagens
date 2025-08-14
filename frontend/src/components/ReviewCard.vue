<template>
  <div class="review-card">
    <div class="card-header">
      <div class="author-info">
        <div class="author-avatar">
          <img v-if="review.author.profile_picture" :src="review.author.profile_picture" alt="Foto do autor">
          <i v-else class="fa-solid fa-user"></i>
        </div>
        <div>
          <span class="author-name">{{ review.author.full_name }}</span>
          <span class="review-meta">Avaliou {{ review.offer ? review.offer.title : 'nossa agência' }}</span>
        </div>
      </div>
      <div class="rating-stars">
        <i v-for="n in 5" :key="n" class="fa-star" :class="n <= review.rating ? 'fa-solid' : 'fa-regular'"></i>
      </div>
    </div>
    <div class="card-body">
      <h3 class="review-title">{{ review.title }}</h3>
      <p class="review-content">{{ review.content }}</p>
      <img v-if="review.photo" :src="review.photo" class="review-photo" alt="Foto da viagem">
    </div>
    <div class="card-footer">
      <span>{{ formatDate(review.created_at) }}</span>
      <span class="verified-badge"><i class="fa-solid fa-check-circle"></i> Avaliação Verificada</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReviewCard',
  props: { review: { type: Object, required: true } },
  methods: {
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('pt-BR', options);
    }
  }
}
</script>

<style scoped>
.review-card {
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  height: 100%; /* Garante que o card ocupe o espaço da grelha */
}
.card-header { display: flex; justify-content: space-between; align-items: flex-start; padding-bottom: 15px; border-bottom: 1px solid #f0f2f5; }
.author-info { display: flex; align-items: center; gap: 12px; }
.author-avatar { width: 40px; height: 40px; border-radius: 50%; background-color: #f0f2f5; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; color: #6c757d; overflow: hidden; }
.author-avatar img { width: 100%; height: 100%; object-fit: cover; }
.author-name { font-weight: 600; display: block; }
.review-meta { font-size: 0.85rem; color: #6c757d; }
.rating-stars { color: #ffc107; }
.card-body { padding: 15px 0; flex-grow: 1; }
.review-title { font-size: 1.1rem; margin: 0 0 10px 0; }
.review-photo { width: 100%; border-radius: 8px; margin-top: 15px; }
.card-footer { padding-top: 15px; border-top: 1px solid #f0f2f5; display: flex; justify-content: space-between; font-size: 0.8rem; color: #6c757d; }
.verified-badge { color: #198754; font-weight: 500; }
</style>
