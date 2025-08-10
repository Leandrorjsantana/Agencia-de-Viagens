<template>
  <div class="home-page-container" v-if="pageData">
    <!-- Seção de Banners (Ainda não funcional, apenas a estrutura) -->
    <section class="banner-placeholder">
      <div class="container">
        <h1>O seu próximo destino começa aqui.</h1>
        <p>Encontre as melhores ofertas em pacotes, hotéis e voos.</p>
      </div>
    </section>

    <!-- Barra de Serviços (Ainda não funcional, apenas a estrutura) -->
    <div class="services-bar">
      <div class="container">
        <div v-for="service in pageData.services" :key="service.id" class="service-item">
          <i :class="service.icon_class"></i>
          <span>{{ service.name }}</span>
        </div>
      </div>
    </div>

    <!-- Conteúdo principal -->
    <div class="container main-content">
      <h2>Página Inicial da Agência</h2>
      <p>Se você está vendo esta mensagem, o layout principal e a página inicial estão conectados com sucesso.</p>
      <p>Nosso próximo passo será preencher esta área com os carrosséis de ofertas e o formulário de busca, usando os dados que vêm do seu painel de administração.</p>
    </div>
  </div>
  <div v-else class="loading-placeholder">
    <p>Carregando conteúdo da página inicial...</p>
  </div>
</template>

<script>
export default {
  name: 'HomeView', // O nome do componente deve ser HomeView para corresponder ao nome do arquivo
  props: {
    pageData: Object,
    backendUrl: String,
  }
}
</script>

<style scoped>
/* Estilos para a nossa nova página inicial */
.banner-placeholder {
  background-color: #333;
  color: white;
  padding: 100px 0;
  text-align: center;
}

.services-bar {
  background-color: #fff;
  padding: 20px 0;
  border-bottom: 1px solid #eee;
}

.services-bar .container {
  display: flex;
  justify-content: center;
  gap: 40px;
}

.service-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  font-weight: 500;
}

.service-item i {
  font-size: 2rem;
  color: var(--primary-color);
}

.main-content {
  padding: 60px 20px;
  text-align: center;
}

.loading-placeholder {
  text-align: center;
  padding: 100px;
}
</style>