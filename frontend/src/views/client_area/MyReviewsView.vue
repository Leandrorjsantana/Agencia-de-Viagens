<template>
  <div class="my-reviews-page">
    <div class="page-header">
      <h1>Minhas Avaliações</h1>
      <p>Veja, edite ou partilhe uma nova experiência de viagem.</p>
    </div>
    <div class="header-actions">
      <router-link to="/area-cliente/avaliacoes/nova" class="cta-button">
        <i class="fa-solid fa-plus"></i> Deixar Nova Avaliação
      </router-link>
    </div>
    <div v-if="loading" class="loading-spinner"><p>A carregar as suas avaliações...</p></div>
    <div v-if="!loading && reviews.length > 0" class="reviews-list">
      <div v-for="review in reviews" :key="review.id" class="review-item">
        <div class="review-content">
          <h4>{{ review.title }}</h4>
          <p>"{{ review.content ? review.content.substring(0, 100) : '' }}..."</p>
          <div class="review-meta">
            <span>Para: {{ review.offer ? review.offer.title : 'Avaliação da Agência' }}</span>
            <span>Nota: {{ review.rating }} de 5 estrelas</span>
          </div>
        </div>
        <div class="review-actions">
          <button class="action-btn edit-btn"><i class="fa-solid fa-pencil"></i> Editar</button>
          <button class="action-btn delete-btn"><i class="fa-solid fa-trash"></i> Apagar</button>
        </div>
      </div>
    </div>
    <div v-if="!loading && reviews.length === 0" class="no-reviews-message">
      <p>Você ainda não deixou nenhuma avaliação.</p>
    </div>
  </div>
</template>

<script>
// ... (seu script existente)
</script>

<style scoped>
/* ... (seus estilos existentes) ... */
.review-actions {
  display: flex;
  gap: 10px;
}
.action-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 5px;
}
.edit-btn {
  background-color: #ffc107;
  color: #000;
}
.delete-btn {
  background-color: #dc3545;
  color: #fff;
}
</style>