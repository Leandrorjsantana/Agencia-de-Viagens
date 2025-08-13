<template>
  <div class="post-detail-page">
    <div v-if="loading" class="loading-container">
      <p>A carregar o artigo...</p>
    </div>

    <div v-if="!loading && post" class="container page-content">
      <div class="blog-layout">
        <!-- Coluna Principal: Conteúdo do Post -->
        <main class="main-content">
          <article class="post-article">
            <header class="post-header">
              <div class="post-meta-top" v-if="post.category">
                <router-link :to="`/blog/categoria/${post.category.slug}`" class="post-category">{{ post.category.name }}</router-link>
              </div>
              <h1 class="post-title">{{ post.title }}</h1>
              <div class="post-meta-bottom">
                <span v-if="post.author">Por {{ post.author.full_name }}</span>
                <span>{{ formatDate(post.published_at) }}</span>
              </div>
            </header>
            
            <div class="featured-image-container">
              <img :src="getMediaUrl(post.featured_image)" :alt="post.title">
            </div>

            <div class="post-body" v-html="post.content"></div>

            <footer class="post-footer">
              <div class="share-section">
                <strong>Gostou deste artigo? Partilhe!</strong>
                <div class="share-buttons">
                  <a :href="shareLinks.facebook" target="_blank" rel="noopener noreferrer" class="share-btn facebook"><i class="fab fa-facebook-f"></i></a>
                  <a :href="shareLinks.twitter" target="_blank" rel="noopener noreferrer" class="share-btn twitter"><i class="fab fa-twitter"></i></a>
                  <a :href="shareLinks.whatsapp" target="_blank" rel="noopener noreferrer" class="share-btn whatsapp"><i class="fab fa-whatsapp"></i></a>
                  <a :href="shareLinks.linkedin" target="_blank" rel="noopener noreferrer" class="share-btn linkedin"><i class="fab fa-linkedin-in"></i></a>
                </div>
              </div>
              <router-link to="/blog" class="back-to-blog-button">
                <i class="fa-solid fa-arrow-left"></i> Voltar para o Blog
              </router-link>
            </footer>
          </article>

          <!-- Secção de Comentários -->
          <section class="comments-section">
            <h2 class="section-title">{{ comments.length }} Comentários</h2>
            <div v-if="isLoggedIn" class="comment-form">
              <h3>Deixe o seu comentário</h3>
              <form @submit.prevent="submitComment">
                <textarea v-model="newComment" placeholder="Escreva a sua mensagem..." required></textarea>
                <button type="submit" :disabled="isSubmittingComment">
                  {{ isSubmittingComment ? 'A enviar...' : 'Enviar Comentário' }}
                </button>
              </form>
            </div>
            <div v-else class="login-prompt">
              <p>Você precisa de <router-link :to="`/login?redirect=${$route.fullPath}`">fazer login</router-link> para comentar.</p>
            </div>
            <div class="comments-list">
              <div v-for="comment in comments" :key="comment.id" class="comment-item">
                <div class="comment-author">{{ comment.author.full_name }}</div>
                <div class="comment-date">{{ formatDate(comment.created_at) }}</div>
                <p class="comment-content">{{ comment.content }}</p>
              </div>
            </div>
          </section>

          <!-- Secção de Posts Relacionados -->
          <section v-if="post.related_posts && post.related_posts.length > 0" class="related-posts-section">
            <h2 class="section-title">Inspire-se com Mais Conteúdo</h2>
            <div class="related-posts-grid">
              <PostCard 
                v-for="relatedPost in post.related_posts" 
                :key="relatedPost.id" 
                :post="relatedPost" 
              />
            </div>
          </section>
        </main>

        <!-- Barra Lateral -->
        <aside class="sidebar">
          <div v-if="sidebarLoading" class="loading-spinner"><p>A carregar...</p></div>
          <div v-if="!sidebarLoading && sidebarData">
            <div class="widget">
              <h3 class="widget-title">Posts Recentes</h3>
              <ul class="recent-posts-list">
                <li v-for="recentPost in sidebarData.recent_posts" :key="recentPost.slug">
                  <router-link :to="`/blog/${recentPost.slug}`" class="recent-post-item">
                    <img :src="getMediaUrl(recentPost.featured_image)" alt="">
                    <span>{{ recentPost.title }}</span>
                  </router-link>
                </li>
              </ul>
            </div>
            <div class="widget">
              <h3 class="widget-title">Categorias</h3>
              <ul class="categories-list">
                <li v-for="cat in sidebarData.categories" :key="cat.slug">
                  <router-link :to="`/blog/categoria/${cat.slug}`">
                    <span>{{ cat.name }}</span>
                    <span class="count">{{ cat.post_count }}</span>
                  </router-link>
                </li>
              </ul>
            </div>
            <div class="widget" v-if="sidebarData.ad_banners && sidebarData.ad_banners.length > 0">
              <h3 class="widget-title">Publicidade</h3>
              <div class="ad-banners">
                <a v-for="(banner, index) in sidebarData.ad_banners" :key="index" :href="banner.link_url" target="_blank" rel="noopener noreferrer">
                  <img :src="getMediaUrl(banner.image)" alt="Publicidade">
                </a>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <div v-if="error" class="error-message container">
      <h2>Post Não Encontrado</h2>
      <router-link to="/blog" class="back-home-button">Voltar ao Blog</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL, getMediaUrl } from '../config';
import PostCard from '../components/PostCard.vue';

export default {
  name: 'PostDetailView',
  components: { PostCard },
  data() {
    return {
      post: null,
      sidebarData: null,
      comments: [],
      loading: true,
      sidebarLoading: true,
      error: false,
      backendUrl: BACKEND_URL,
      isLoggedIn: false,
      newComment: '',
      isSubmittingComment: false,
    };
  },
  watch: {
    '$route.params.slug': {
      immediate: true,
      handler() {
        this.fetchPostDetails();
      }
    }
  },
  computed: {
    shareLinks() {
      const url = window.location.href;
      const title = this.post ? this.post.title : '';
      return {
        facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
        twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
        whatsapp: `https://api.whatsapp.com/send?text=${encodeURIComponent(title + ' ' + url)}`,
        linkedin: `https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(url)}&title=${encodeURIComponent(title)}`,
      };
    }
  },
  methods: {
    getMediaUrl,
    getAuthHeaders() {
      const token = localStorage.getItem('accessToken');
      if (!token) return {};
      return { 'Authorization': `Bearer ${token}` };
    },
    checkLoginStatus() {
      this.isLoggedIn = !!localStorage.getItem('accessToken');
    },
    async fetchPostDetails() {
      this.loading = true;
      this.error = false;
      const slug = this.$route.params.slug;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/blog/posts/${slug}/`);
        this.post = response.data;
        document.title = this.post.title;
        await this.fetchComments();
      } catch (err) {
        this.error = true;
        console.error("Erro ao buscar detalhes do post:", err);
      } finally {
        this.loading = false;
      }
    },
    async fetchSidebarData() {
      this.sidebarLoading = true;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/blog/sidebar-data/`);
        this.sidebarData = response.data;
      } catch (error) {
        console.error("Erro ao buscar dados da sidebar:", error);
      } finally {
        this.sidebarLoading = false;
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('pt-BR', options);
    },
    async fetchComments() {
      const slug = this.$route.params.slug;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/blog/posts/${slug}/comments/`);
        this.comments = response.data;
      } catch (error) {
        console.error("Erro ao buscar comentários:", error);
      }
    },
    async submitComment() {
      if (!this.newComment.trim()) return;
      this.isSubmittingComment = true;
      const slug = this.$route.params.slug;
      try {
        await axios.post(
          `${this.backendUrl}/api/v1/blog/posts/${slug}/comments/`,
          { content: this.newComment },
          { headers: this.getAuthHeaders() }
        );
        this.newComment = '';
        await this.fetchComments();
      } catch (error) {
        alert("Ocorreu um erro ao enviar o seu comentário. Tente novamente.");
        console.error("Erro ao submeter comentário:", error);
      } finally {
        this.isSubmittingComment = false;
      }
    }
  },
  created() {
    this.checkLoginStatus();
    this.fetchSidebarData();
  }
};
</script>

<style scoped>
.page-content { padding: 50px 20px; }
.blog-layout { display: grid; grid-template-columns: 1fr; gap: 40px; }
@media (min-width: 992px) { .blog-layout { grid-template-columns: 2fr 1fr; } }
.post-article { background: #fff; padding: 30px; border-radius: 8px; }
.post-header { text-align: center; margin-bottom: 30px; }
.post-category { display: inline-block; background-color: var(--primary-color); color: #fff; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; font-weight: 500; text-decoration: none; margin-bottom: 15px; }
.post-title { font-size: 2.5rem; font-weight: 700; margin: 0 0 15px 0; }
.post-meta-bottom { color: #777; }
.post-meta-bottom span:not(:last-child)::after { content: '•'; margin: 0 10px; }
.featured-image-container { margin-bottom: 30px; }
.featured-image-container img { width: 100%; border-radius: 12px; }
.post-body { line-height: 1.8; font-size: 1.1rem; }
.post-body ::v-deep(p) { margin-bottom: 1.5em; }
.post-body ::v-deep(h2) { font-size: 1.8rem; margin-top: 1.5em; margin-bottom: 0.8em; }
.post-body ::v-deep(ul) { padding-left: 25px; margin-bottom: 1.5em; }
.post-body ::v-deep(blockquote) { border-left: 4px solid var(--primary-color); padding-left: 20px; margin: 2em 0; font-style: italic; color: #666; }
.post-footer { margin-top: 40px; padding-top: 30px; border-top: 1px solid #eee; display: flex; flex-direction: column; align-items: center; gap: 30px; }
.share-section { text-align: center; }
.share-section strong { display: block; margin-bottom: 15px; font-size: 1.1rem; }
.share-buttons { display: flex; gap: 15px; }
.share-btn { width: 40px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: #fff; text-decoration: none; font-size: 1.1rem; transition: transform 0.2s; }
.share-btn:hover { transform: scale(1.1); }
.share-btn.facebook { background-color: #1877F2; }
.share-btn.twitter { background-color: #1DA1F2; }
.share-btn.whatsapp { background-color: #25D366; }
.share-btn.linkedin { background-color: #0A66C2; }
.back-to-blog-button { display: inline-flex; align-items: center; gap: 10px; padding: 12px 25px; background-color: #f0f2f5; color: #333; border-radius: 50px; text-decoration: none; font-weight: bold; transition: background-color 0.2s; }
.back-to-blog-button:hover { background-color: #e0e0e0; }
.comments-section { margin-top: 50px; padding-top: 30px; border-top: 1px solid #eee; }
.section-title { font-size: 1.8rem; margin-bottom: 30px; }
.comment-form { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
.comment-form textarea { width: 100%; min-height: 100px; padding: 10px; border: 1px solid #ccc; border-radius: 5px; margin-bottom: 10px; }
.comment-form button { background: var(--primary-color); color: #fff; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
.login-prompt { text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px; margin-bottom: 30px; }
.comments-list { display: flex; flex-direction: column; gap: 25px; }
.comment-item { border-bottom: 1px solid #eee; padding-bottom: 15px; }
.comment-author { font-weight: bold; }
.comment-date { font-size: 0.8rem; color: #777; margin-bottom: 10px; }
.related-posts-section { margin-top: 50px; padding-top: 30px; border-top: 1px solid #eee; }
.related-posts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }
.sidebar .widget { background: #fff; padding: 20px; border-radius: 8px; margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.widget-title { font-size: 1.2rem; margin: 0 0 15px 0; padding-bottom: 10px; border-bottom: 1px solid #eee; }
.recent-posts-list { list-style: none; padding: 0; margin: 0; }
.recent-post-item { display: flex; align-items: center; gap: 15px; margin-bottom: 15px; text-decoration: none; color: #333; }
.recent-post-item:hover span { color: var(--primary-color); }
.recent-post-item img { width: 60px; height: 60px; object-fit: cover; border-radius: 5px; flex-shrink: 0; }
.categories-list { list-style: none; padding: 0; margin: 0; }
.categories-list a { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f0f0f0; text-decoration: none; color: #555; font-weight: 500; }
.categories-list a:hover span { color: var(--primary-color); }
.categories-list .count { background: #eee; padding: 2px 8px; border-radius: 20px; font-size: 0.8rem; }
.ad-banners img { width: 100%; border-radius: 5px; margin-bottom: 15px; }
.error-message { text-align: center; padding: 50px; }
.back-home-button { display: inline-block; margin-top: 20px; padding: 12px 25px; background-color: var(--primary-color); color: #fff; border-radius: 50px; text-decoration: none; font-weight: bold; }
</style>
