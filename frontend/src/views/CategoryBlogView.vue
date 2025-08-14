<template>
  <div class="blog-page">
    <div class="page-header" :style="headerStyle">
      <div class="container">
        <h1>Categoria: {{ categoryName }}</h1>
        <p>A explorar todos os artigos sobre {{ categoryName }}.</p>
      </div>
    </div>

    <div class="container page-content">
      <div class="blog-layout">
        <main class="main-content">
          <div v-if="loading" class="loading-spinner"><p>A carregar posts...</p></div>
          <div v-if="!loading && posts.length > 0" class="posts-grid">
            <PostCard 
              v-for="post in posts" 
              :key="post.id" 
              :post="post" 
            />
          </div>
          <div v-if="!loading && posts.length === 0" class="no-posts-message">
            <p>Nenhum post encontrado para esta categoria no momento.</p>
          </div>
        </main>

        <aside class="sidebar">
          <div v-if="sidebarLoading" class="loading-spinner"><p>A carregar...</p></div>
          <div v-if="!sidebarLoading && sidebarData">
            <div class="widget">
              <h3 class="widget-title">Posts Recentes</h3>
              <ul class="recent-posts-list">
                <li v-for="post in sidebarData.recent_posts" :key="post.slug">
                  <router-link :to="`/blog/${post.slug}`" class="recent-post-item">
                    <img :src="getMediaUrl(post.featured_image)" alt="">
                    <span>{{ post.title }}</span>
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
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL, getMediaUrl } from '../config';
import PostCard from '../components/PostCard.vue';

export default {
  name: 'CategoryBlogView',
  components: { PostCard },
  props: {
    pageData: Object,
  },
  data() {
    return {
      posts: [],
      sidebarData: null,
      loading: true,
      sidebarLoading: true,
      backendUrl: BACKEND_URL,
      categoryName: ''
    };
  },
  computed: {
    headerStyle() {
      const config = this.pageData?.site_configuration;
      if (config && config.page_header_bg_color) {
        return { backgroundColor: config.page_header_bg_color };
      }
      return { backgroundColor: '#003366' };
    }
  },
  watch: {
    '$route.params.slug': {
      immediate: true,
      handler() {
        this.fetchCategoryPosts();
      }
    }
  },
  methods: {
    getMediaUrl,
    // ===== AJUSTE PRINCIPAL AQUI =====
    async fetchCategoryPosts() {
      this.loading = true;
      const slug = this.$route.params.slug;
      try {
        // REVERTIDO: Voltando para a URL da API que estava correta e funcional
        const response = await axios.get(`${this.backendUrl}/api/v1/blog/categoria/${slug}/`);
        this.posts = response.data;
        
        // Mantendo a lógica original para pegar o nome da categoria
        if (this.posts.length > 0 && this.posts[0].category && this.posts[0].category.name) {
          this.categoryName = this.posts[0].category.name;
        } else {
            // Se não encontrar, usa o slug da URL como fallback
            const formattedSlug = slug.replace(/-/g, ' ');
            this.categoryName = formattedSlug.charAt(0).toUpperCase() + formattedSlug.slice(1);
        }
      } catch (error) {
        console.error("Erro ao buscar os posts da categoria:", error);
        this.posts = [];
        this.categoryName = "Categoria não encontrada";
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
    }
  },
  created() {
    this.fetchSidebarData();
  }
};
</script>

<style scoped>
/* Estilos mantidos, pois já estavam corretos */
.page-header { 
  padding: 50px 0; 
  text-align: center; 
  border-bottom: 1px solid #e9ecef;
  color: #fff;
}
.page-header h1 { font-size: 2.8rem; }
.page-content { padding: 50px 20px; }
.blog-layout { display: grid; grid-template-columns: 1fr; gap: 40px; }
@media (min-width: 992px) { .blog-layout { grid-template-columns: 2fr 1fr; } }
.posts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; align-items: stretch; }
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
</style>