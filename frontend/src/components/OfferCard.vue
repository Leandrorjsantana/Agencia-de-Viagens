<template>
  <div class="offer-card">
    <div class="offer-image-container">
      <img :src="imageUrl" :alt="offer.subtitle || offer.title || 'Oferta'">
      <div class="duration-on-image" v-if="offer.duration_days">
        <span>{{ offer.duration_days }} DIAS / {{ offer.duration_nights }} NOITES</span>
      </div>
    </div>

    <div class="card-content">
      <div class="card-content-top">
        <span v-if="offer.promo_tag" class="promo-tag">{{ offer.promo_tag }}</span>
        <span class="package-details-card" v-if="offer.subtitle">{{ offer.subtitle }}</span>
        <h3 class="offer-title-card">{{ offer.title }}</h3>

        <div class="hotel-info" v-if="offer.hotel_name">
          <span v-if="offer.hotel_rating" class="hotel-rating">{{ offer.hotel_rating }}</span>
          <span class="hotel-name">{{ offer.hotel_name }}</span>
        </div>

        <p class="origin-card" v-if="offer.origin"><i class="fa-solid fa-plane-departure"></i> Saindo de {{ offer.origin }}</p>

        <div class="offer-includes" v-if="offer.details">
          <p v-for="(item, index) in splitDetails" :key="index">
            <i class="fa-solid fa-check" aria-hidden="true"></i>
            <span class="include-text">{{ item }}</span>
          </p>
        </div>
      </div>

      <div class="card-content-bottom">
        <div class="price-section">
          <div class="savings-highlight" v-if="offer.original_price && offer.original_price > offer.price">
            Economize R$ {{ formatPrice(offer.original_price - offer.price) }}
          </div>
          <div class="price-original-line" v-if="offer.original_price">
            <span class="original-price">R$ {{ formatPrice(offer.original_price) }}</span>
          </div>
          <span class="price-label">{{ offer.price_per_person ? 'Preço por pessoa' : '' }}</span>

          <div class="price-final-line">
            <span class="price-currency">R$</span>
            <span class="price-value">{{ formatPrice(offer.price) }}</span>
          </div>

          <span class="taxes-info">{{ offer.taxes_included ? 'Taxas e impostos inclusos' : 'Taxas e impostos não inclusos' }}</span>
        </div>

        <router-link :to="`/ofertas/${offer.slug}`" class="details-button" :class="{ highlighted: offer.highlight_button }">Ver oferta</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OfferCard',
  props: {
    offer: { type: Object, required: true },
    backendUrl: {
      type: String,
      required: false,
      default: ''
    }
  },
  computed: {
    imageUrl() {
      if (!this.offer || !this.offer.image) return '/placeholder.jpg';
      const img = this.offer.image;
      if (/^https?:\/\//i.test(img)) return img;
      const base = (this.backendUrl || '').replace(/\/+$/,'');
      const prefix = img.startsWith('/') ? '' : '/';
      return base ? `${base}${prefix}${img}` : `${prefix}${img}`;
    },
    splitDetails() {
      if (!this.offer || !this.offer.details) return [];
      return String(this.offer.details).split(/\r?\n/).map(s => s.trim()).filter(Boolean);
    }
  },
  methods: {
    formatPrice(value) {
      const num = parseFloat(value);
      if (isNaN(num)) return value || '0';
      return new Intl.NumberFormat('pt-BR').format(num);
    }
  }
};
</script>

<style scoped>
/* O seu CSS original, com o ajuste fino para o alinhamento */
* { box-sizing: border-box; }

.offer-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
  transition: transform .15s ease, box-shadow .15s ease;
}
.offer-card:hover { transform: translateY(-6px); box-shadow: 0 14px 40px rgba(0,0,0,0.12); }

.offer-image-container { position: relative; width: 100%; }
.offer-image-container img { width: 100%; height: 200px; object-fit: cover; display: block; }

.duration-on-image {
  position: absolute;
  bottom: 10px;
  left: 10px;
  background-color: rgba(0,0,0,0.6);
  color: #fff;
  padding: 6px 10px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.8rem;
}

.card-content { padding: 18px; display: flex; flex-direction: column; flex: 1 1 auto; }
.card-content-top { flex: 1 1 auto; }

/* --- CORREÇÃO AQUI --- */
.card-content-bottom {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  /* Organiza os itens em coluna */
  flex-direction: column;
  /* Alinha tudo à direita */
  align-items: flex-end;
}
.price-section {
  text-align: right;
  width: 100%; /* Garante que o alinhamento à direita funcione */
  margin-bottom: 15px; /* Adiciona espaço entre o preço e o botão */
}
.details-button {
  display: inline-block;
  width: auto; /* O botão agora tem a largura do seu conteúdo */
  min-width: 150px; /* Garante uma largura mínima para o botão */
  padding: 12px 20px;
  border-radius: 8px;
  text-align: center;
  background-color: var(--primary-color);
  color: #fff;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s ease;
}
/* --- FIM DA CORREÇÃO --- */

.promo-tag { display: inline-block; margin-bottom: 10px; background-color: #eafbe9; color: #066b3a; padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 0.8rem; }
.package-details-card { display: block; font-size: 0.9rem; color: #666; margin-bottom: 6px; text-transform: uppercase; font-weight: 600; }
.offer-title-card { font-size: 1.1rem; color: #111; margin: 0 0 10px 0; font-weight: 700; line-height: 1.25; }
.hotel-info { display: flex; gap: 8px; align-items: center; font-size: 0.9rem; margin-bottom: 8px; }
.hotel-rating { background-color: #003366; color: #fff; padding: 4px 8px; border-radius: 4px; font-weight: 700; font-size: 0.85rem; }
.origin-card { font-size: 0.9rem; color: #666; margin: 8px 0; display: flex; gap: 8px; align-items: center; }
.offer-includes { font-size: 0.9rem; color: #555; line-height: 1.6; margin-top: 6px; }
.offer-includes p { margin: 0 0 6px 0; display: flex; align-items: flex-start; gap: 8px; }
.offer-includes .fa-check { color: #198754; margin-top: 3px; }
.savings-highlight { background-color: #dff6e9; color: #066b3a; padding: 4px 8px; border-radius: 6px; font-weight: 700; font-size: 0.85rem; display: inline-block; margin-bottom: 6px; }
.price-original-line { font-size: 0.9rem; color: #777; }
.original-price { text-decoration: line-through; margin-right: 6px; }
.price-label { font-size: 0.8rem; color: #777; display: block; margin-top: 4px; }
.price-final-line { display: flex; align-items: baseline; gap: 6px; justify-content: flex-end; }
.price-currency { font-size: 0.95rem; font-weight: 600; }
.price-value { font-size: 1.7rem; font-weight: 800; color: var(--primary-color); }
.taxes-info { font-size: 0.75rem; color: #777; display:block; margin-top:4px; }
.details-button.highlighted { background-color: #ffc107; color: #000; }
.details-button:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
</style>