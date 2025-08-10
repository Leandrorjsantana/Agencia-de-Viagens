<template>
  <div class="client-area-container">
    <aside class="sidebar">
      <div class="sidebar-header">
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
        <a href="#" @click.prevent="logout" class="nav-link logout-link">
          <i class="fa-solid fa-sign-out-alt"></i>
          <span>Sair</span>
        </a>
      </nav>
    </aside>
    <main class="main-content">
      <router-view :backendUrl="backendUrl" />
    </main>
  </div>
</template>

<script>
export default {
  name: 'ClientAreaLayout',
  props: {
    backendUrl: String,
  },
  methods: {
    logout() {
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.client-area-container {
  display: flex;
  min-height: calc(100vh - 150px); /* Ajuste conforme a altura do seu cabeçalho/rodapé */
}
.sidebar {
  width: 260px;
  background-color: #ffffff;
  border-right: 1px solid #e0e0e0;
  padding: 25px;
  flex-shrink: 0;
}
.sidebar-header h3 {
  font-size: 1.5rem;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
  text-align: center;
  color: #333;
}
.sidebar-nav {
  display: flex;
  flex-direction: column;
  height: calc(100% - 80px); /* Preenche o espaço vertical */
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
  margin-top: auto; /* Empurra o link de sair para o final */
}
.main-content {
  flex-grow: 1;
  padding: 40px;
  background-color: #f4f5f7;
}
</style>