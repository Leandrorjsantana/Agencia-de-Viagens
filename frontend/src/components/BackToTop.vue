<template>
  <button v-show="visible" class="back-to-top" @click="scrollToTop" aria-label="Voltar ao topo">
    ↑
  </button>
</template>

<script>
export default {
  data() {
    return {
      visible: false,
    };
  },
  methods: {
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    checkScroll() {
      this.visible = window.pageYOffset > 300;
    }
  },
  mounted() {
    window.addEventListener('scroll', this.checkScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.checkScroll);
  }
}
</script>

<style scoped>
.back-to-top {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: var(--primary-color, #003366);
  color: white;
  border: none;
  border-radius: 50%;
  width: 44px;
  height: 44px;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
  opacity: 0.7;
  transition: opacity 0.3s;
  z-index: 9999;
}
.back-to-top:hover {
  opacity: 1;
}
</style>
