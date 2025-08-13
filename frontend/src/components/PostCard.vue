<template>
  <!-- Adicionamos uma classe condicional para o post fixado -->
  <router-link :to="`/blog/${post.slug}`" class="post-card" :class="{ 'is-pinned': post.is_pinned }">
    <div class="post-image-container">
      <img :src="getMediaUrl(post.featured_image)" :alt="post.title">
      <!-- NOVO: Ícone de "Fixado" que aparece sobre a imagem -->
      <div v-if="post.is_pinned" class="pinned-badge">
        <i class="fa-solid fa-thumbtack"></i>
        <span>Destaque</span>
      </div>
    </div>
    <div class="post-content">
      <div class="post-meta">
        <span class="post-category" v-if="post.category">{{ post.category.name }}</span>
        <span class="post-date">{{ formatDate(post.published_at) }}</span>
      </div>
      <h3 class="post-title">{{ post.title }}</h3>
      <p class="post-summary">{{ post.summary }}</p>
      <div class="read-more">
        Leia Mais <i class="fa-solid fa-arrow-right"></i>
      </div>
    </div>
  </router-link>
</template>

<script>
import { getMediaUrl } from '../config';

export default {
  name: 'PostCard',
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
  methods: {
    getMediaUrl,
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('pt-BR', options);
    }
  }
}
</script>

<style scoped>
.post-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 6px 25px rgba(0,0,0,0.08);
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  overflow: hidden;
  height: 100%;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 2px solid transparent; /* Borda inicial transparente */
}
.post-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 35px rgba(0,0,0,0.12);
}

/* --- NOVOS ESTILOS PARA O POST FIXADO --- */
.post-card.is-pinned {
  border-color: var(--primary-color); /* Adiciona uma borda colorida */
}
.pinned-badge {
  position: absolute;
  top: 15px;
  left: 15px;
  background-color: var(--primary-color);
  color: #fff;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 6px;
}
/* --- FIM DOS NOVOS ESTILOS --- */

.post-image-container {
  position: relative; /* Necessário para o badge de "Fixado" */
  width: 100%;
  height: 200px;
  background-color: #f0f2f5;
}
.post-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.post-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}
.post-meta {
  display: flex;
  gap: 15px;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 10px;
}
.post-category {
  background-color: var(--primary-color);
  color: #fff;
  padding: 3px 10px;
  border-radius: 20px;
  font-weight: 500;
}
.post-title {
  font-size: 1.25rem;
  margin: 0 0 10px 0;
  line-height: 1.4;
}
.post-summary {
  font-size: 0.95rem;
  line-height: 1.6;
  flex-grow: 1;
}
.read-more {
  margin-top: 15px;
  color: var(--primary-color);
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
