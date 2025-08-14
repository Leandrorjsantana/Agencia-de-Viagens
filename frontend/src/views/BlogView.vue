<template>
  <div class="blog-page">
    <div class="page-header" :style="headerStyle">
      <div class="container">
        <h1>{{ pageData?.site_configuration?.blog_page_title || 'Nosso Blog' }}</h1>
        <p>{{ pageData?.site_configuration?.blog_page_subtitle || 'Dicas, novidades e inspirações para a sua próxima viagem.' }}</p>
      </div>
    </div>

    <div class="container page-content">
      <div class="blog-layout">
        <main class="main-content">
          <div v-if="loading" class="loading-spinner"><p>A carregar posts...</p></div>
          <div v-if="!loading && posts.length > 0" class="blog-grid">
            <PostCard 
              v-for="post in posts" 
              :key="post.id" 
              :post="post" 
            />
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
  name: 'BlogView',
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
    };
  },
  computed: {
    headerStyle() {
      const config = this.pageData?.site_configuration;
      if (config && config.page_header_bg_color) {
        return { backgroundColor: config.page_header_bg_color };
      }
      return { backgroundColor: '#f8f9fa' };
    }
  },
  async created() {
    this.fetchPosts();
    this.fetchSidebarData();
  },
  methods: {
    getMediaUrl,
    async fetchPosts() {
      this.loading = true;
      try {
        const response = await axios.get(`${this.backendUrl}/api/v1/blog/posts/`);
        this.posts = response.data;
      } catch (error) {
        console.error("Erro ao buscar os posts:", error);
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
  }
};
</script>

<style scoped>
.page-header {
  padding: 30px 0;
  text-align: center;
  border-bottom: 1px solid #e9ecef;
  /* AJUSTE: Adicionando a cor branca para a fonte, como nas outras páginas */
  color: #fff;
}
.page-header h1 { font-size: 2.6rem; }
.page-header p { font-size: 0.95rem; }

.page-content {
  padding: 30px 15px;
}

.blog-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 30px;
}
@media (min-width: 992px) {
  .blog-layout {
    grid-template-columns: 2fr 1fr;
  }
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  align-items: stretch;
}
@media (min-width: 1400px) {
  .posts-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.sidebar .widget {
  background: #fff;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 1px 5px rgba(0,0,0,0.05);
}
.widget-title {
  font-size: 1rem;
  margin: 0 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}
.recent-posts-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.recent-post-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  text-decoration: none;
  color: #333;
}
.recent-post-item:hover span {
  color: var(--primary-color);
}
.recent-post-item img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 5px;
  flex-shrink: 0;
}
.categories-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.categories-list a {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  text-decoration: none;
  color: #555;
  font-weight: 500;
}
.categories-list a:hover span {
  color: var(--primary-color);
}
.categories-list .count {
  background: #eee;
  padding: 2px 6px;
  border-radius: 20px;
  font-size: 0.8rem;
}
.ad-banners img {
  width: 100%;
  border-radius: 5px;
  margin-bottom: 10px;
}
</style>