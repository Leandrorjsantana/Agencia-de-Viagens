<template>
  <section class="promotion-section">
    <div class="container">
      <h2 class="section-title">Aproveite nossas promoções</h2>
      <div class="cards-grid">
        <a 
          v-for="card in cards" 
          :key="card.id" 
          :href="card.link_url" 
          class="promo-card" 
          target="_blank" 
          rel="noopener noreferrer"
        >
          <div class="image-container">
            <img :src="card.image" alt="Card de promoção">
          </div>
        </a>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'PromotionCards',
  props: {
    cards: {
      type: Array,
      required: true,
      default: () => []
    }
  }
};
</script>

<style scoped>
.promotion-section {
  padding: 40px 0;
  background-color: #f4f5f7;
}

.section-title {
  font-size: 2.0rem;
  font-weight: 700;
  text-align: left;
  margin-bottom: 30px;
  font-family: var(--main-font, 'Poppins', sans-serif);
  color: var(--primary-color, #333);
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.promo-card {
  display: block;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background-color: #ffffff;
}

.promo-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.image-container {
  width: 100%;
  height: 0;
  padding-bottom: 86.53%; /* Proporção da imagem (altura / largura) */
  overflow: hidden;
  position: relative;
  background-color: #eee;
}

.promo-card img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  /* ============================================================= */
  /* CORREÇÃO FINAL: Garante que a imagem está sempre visível */
  /* ============================================================= */
  opacity: 1; 
}

/* --- Media Queries para Responsividade --- */
@media (max-width: 1200px) {
  .cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 992px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
}

@media (max-width: 768px) {
  .cards-grid {
    grid-template-columns: 1fr;
  }
  .section-title {
    font-size: 1.6rem;
    margin-bottom: 20px;
  }
}
</style>