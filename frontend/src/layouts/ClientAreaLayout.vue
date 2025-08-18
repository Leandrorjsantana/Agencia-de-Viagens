<template>
  <div class="client-area-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <router-link to="/" class="sidebar-logo">
          <img
            v-if="logoUrl"
            :key="logoUrl"
            :src="logoUrl"
            alt="Logo da Agência"
            :style="logoStyle"
            @error="handleLogoError"
          />
        </router-link>
        <h3>Minha Conta</h3>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/area-cliente/dashboard" class="nav-link">
          <i class="fa-solid fa-tachometer-alt"></i>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/area-cliente/perfil" class="nav-link">
          <i class="fa-solid fa-user-edit"></i>
          <span>Meu Perfil</span>
        </router-link>
        <router-link to="/area-cliente/reservas" class="nav-link">
          <i class="fa-solid fa-suitcase-rolling"></i>
          <span>Minhas Reservas</span>
        </router-link>
        <router-link to="/area-cliente/avaliacoes/nova" class="nav-link">
          <i class="fa-solid fa-star"></i>
          <span>Deixar Avaliação</span>
        </router-link>
        <a href="#" @click.prevent="logout" class="nav-link logout-link">
          <i class="fa-solid fa-sign-out-alt"></i>
          <span>Sair</span>
        </a>
      </nav>
    </aside>

    <main class="main-content">
      <router-view :pageData="pageData" :backendUrl="backendUrl" />
    </main>
  </div>
</template>

<script>
export default {
  name: 'ClientAreaLayout',
  props: ['pageData', 'backendUrl'],
  data() {
    return {
      logoLoadFailed: false,
    };
  },
  computed: {
    logoUrl() {
      if (this.logoLoadFailed) return '';

      const logo = this.pageData?.site_configuration?.logo;
      if (!logo) return '';

      // Se já veio absoluto do admin (http, https ou //), usa como está
      if (/^https?:\/\//i.test(logo) || /^\/\//.test(logo)) {
        return logo;
      }

      // Caso contrário, junta com backendUrl sem duplicar barras
      const base = String(this.backendUrl || '').replace(/\/+$/, '');
      const path = String(logo).replace(/^\/+/, '');
      if (!base) return `/${path}`; // fallback se backendUrl não foi passado
      return `${base}/${path}`;
    },
    logoStyle() {
      const raw = this.pageData?.site_configuration?.logo_height;
      const h = Number(raw);
      return Number.isFinite(h) && h > 0 ? { maxHeight: `${h}px` } : {};
    },
  },
  methods: {
    handleLogoError() {
      // Esconde o logo quebrado. Se quiser fallback, defina aqui.
      this.logoLoadFailed = true;
      // Exemplo de fallback (descomente se tiver um arquivo estático):
      // this.logoLoadFailed = false;
      // this.$nextTick(() => {
      //   const img = this.$el.querySelector('.sidebar-logo img');
      //   if (img) img.src = '/images/logo-default.png';
      // });
    },
    logout() {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      this.$router.push('/login').then(() => {
        window.location.reload();
      });
    },
  },
  watch: {
    // Se pageData mudar (carregou depois), tenta renderizar de novo
    pageData: {
      handler() {
        this.logoLoadFailed = false;
      },
      deep: true,
    },
  },
};
</script>

<style scoped>
.client-area-container {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 260px;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  padding: 25px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.sidebar-logo {
  display: block;
  margin-bottom: 20px;
}

.sidebar-logo img {
  display: block;
  width: 100%;
  height: auto;
  object-fit: contain;
}

.sidebar-header h3 {
  font-size: 1.5rem;
  color: #333;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.nav-link {
  color: #555;
  text-decoration: none;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 10px;
  transition: background-color 0.3s, color 0.3s;
  display: flex;
  align-items: center;
  font-weight: 500;
}

.nav-link i {
  margin-right: 15px;
  width: 20px;
  text-align: center;
  font-size: 1.1rem;
}

.nav-link:hover {
  background-color: #f4f4f4;
  color: var(--primary-color);
}

.nav-link.router-link-exact-active {
  background-color: var(--primary-color);
  color: #fff;
}

.logout-link {
  margin-top: auto;
}

.main-content {
  flex-grow: 1;
  padding: 40px;
  background-color: #f4f5f7;
  overflow-y: auto;
}
</style>
