<template>
  <div class="exchange-page">
    <div class="page-header" :style="headerStyle">
      <div class="container">
        <h1>Cotações de Moedas Hoje</h1>
        <p v-if="lastUpdate">Última atualização: {{ lastUpdate }}</p>
      </div>
    </div>

    <div class="container page-content">
      <div v-if="loading" class="loading-spinner"><p>A buscar cotações em tempo real...</p></div>
      
      <div v-if="!loading && rates.length > 0" class="exchange-layout">
        <!-- Coluna Principal: Cards de Moedas -->
        <main class="main-content">
          <div class="rates-grid">
            <div v-for="rate in mainRates" :key="rate.code" class="rate-card" :class="rate.code.toLowerCase()">
              <div class="card-header">
                <h3>{{ rate.name.split('/')[0] }} ({{ rate.code }})</h3>
                <span class="rate-variation" :class="getVariationClass(rate.pctChange)">
                  {{ parseFloat(rate.pctChange).toFixed(2) }}%
                  <i class="fa-solid" :class="getVariationIcon(rate.pctChange)"></i>
                </span>
              </div>
              <div class="rate-value">R$ {{ formatValue(rate.bid) }}</div>
              <div class="rate-details">
                <span>Compra: R$ {{ formatValue(rate.bid) }}</span>
                <span>Venda: R$ {{ formatValue(rate.ask) }}</span>
              </div>
            </div>
          </div>
        </main>

        <!-- Barra Lateral: Conversor -->
        <aside class="sidebar">
          <div class="converter-widget">
            <h3>Conversor de Moedas</h3>
            <div class="converter-form">
              <input type="number" v-model="converter.amount" @input="convertCurrency">
              <select v-model="converter.from" @change="convertCurrency">
                <option v-for="currency in allCurrencies" :key="currency.code" :value="currency.code">{{ currency.code }}</option>
              </select>
              <i class="fa-solid fa-right-left swap-icon"></i>
              <select v-model="converter.to" @change="convertCurrency">
                <option v-for="currency in allCurrencies" :key="currency.code" :value="currency.code">{{ currency.code }}</option>
              </select>
            </div>
            <div class="converter-result" v-if="conversionResult">
              <p>{{ converter.amount }} {{ converter.from }} equivale a</p>
              <strong>{{ conversionResult }}</strong>
            </div>
          </div>
        </aside>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { BACKEND_URL } from '../config';

export default {
  name: 'ExchangeView',
  props: { pageData: Object },
  data() {
    return {
      rates: [],
      loading: true,
      converter: {
        amount: 1,
        from: 'USD',
        to: 'BRL',
      },
      conversionResult: null,
    };
  },
  computed: {
    headerStyle() {
      const config = this.pageData?.site_configuration;
      return { backgroundColor: config?.page_header_bg_color || '#003366' };
    },
    lastUpdate() {
      if (this.rates.length > 0) {
        const timestamp = parseInt(this.rates[0].timestamp) * 1000;
        return new Date(timestamp).toLocaleString('pt-BR');
      }
      return '';
    },
    // --- CORREÇÃO AQUI: Seleciona as 4 moedas principais para os cards ---
    mainRates() {
      const mainCodes = ['USD', 'USDT', 'EUR', 'GBP'];
      return this.rates.filter(rate => mainCodes.includes(rate.code));
    },
    allCurrencies() {
      const currencies = this.rates.map(r => ({ code: r.code, bid: parseFloat(r.bid) }));
      if (!currencies.find(c => c.code === 'BRL')) {
        currencies.push({ code: 'BRL', bid: 1 });
      }
      return currencies.sort((a, b) => a.code.localeCompare(b.code));
    },
  },
  methods: {
    async fetchExchangeRates() {
      this.loading = true;
      try {
        const response = await axios.get(`${BACKEND_URL}/api/v1/exchange/rates/`);
        this.rates = response.data;
        this.convertCurrency();
      } catch (error) {
        console.error("Erro ao buscar cotações:", error);
      } finally {
        this.loading = false;
      }
    },
    formatValue(value) {
      return parseFloat(value).toLocaleString('pt-BR', { minimumFractionDigits: 4 });
    },
    getVariationClass(pctChange) {
      return parseFloat(pctChange) >= 0 ? 'positive' : 'negative';
    },
    getVariationIcon(pctChange) {
      return parseFloat(pctChange) >= 0 ? 'fa-arrow-up' : 'fa-arrow-down';
    },
    convertCurrency() {
      if (!this.converter.amount || this.rates.length === 0) {
        this.conversionResult = null;
        return;
      }
      const fromRate = this.allCurrencies.find(c => c.code === this.converter.from).bid;
      const toRate = this.allCurrencies.find(c => c.code === this.converter.to).bid;
      const result = (this.converter.amount * fromRate) / toRate;
      this.conversionResult = `${result.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${this.converter.to}`;
    }
  },
  created() {
    this.fetchExchangeRates();
  }
}
</script>

<style scoped>
.page-header { padding: 60px 0; color: #fff; text-align: center; }
.page-header h1 { font-size: 2.8rem; }
.page-header p { font-size: 1rem; margin-top: 10px; opacity: 0.8; }
.page-content { padding: 50px 20px; }
.exchange-layout { display: grid; grid-template-columns: 1fr; gap: 40px; }
@media (min-width: 992px) { .exchange-layout { grid-template-columns: 2fr 1fr; } }

/* --- CORREÇÃO AQUI: Ajustando a grelha para 4 colunas --- */
.rates-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}
@media (min-width: 768px) {
  .rates-grid {
    grid-template-columns: 1fr 1fr;
  }
}
@media (min-width: 1200px) {
  .rates-grid {
    grid-template-columns: 1fr 1fr; /* Mantém 2x2 para melhor visualização */
  }
}

.rate-card { padding: 20px; border-radius: 12px; color: #fff; box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
.rate-card.usd { background: linear-gradient(45deg, #007bff, #0056b3); }
.rate-card.usdt { background: linear-gradient(45deg, #28a745, #20c997); } /* Nova cor para Dólar Turismo */
.rate-card.eur { background: linear-gradient(45deg, #17a2b8, #117a8b); }
.rate-card.gbp { background: linear-gradient(45deg, #6610f2, #4a09a5); }

.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.card-header h3 { margin: 0; font-size: 1.2rem; }
.rate-value { font-size: 2.2rem; font-weight: 700; }
.rate-variation { font-weight: 500; }
.rate-variation.positive { color: #c8e6c9; }
.rate-variation.negative { color: #ffcdd2; }
.rate-details { font-size: 0.9rem; opacity: 0.8; display: flex; justify-content: space-between; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px; }

.sidebar .converter-widget { background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
.converter-form { display: grid; grid-template-columns: 1fr; gap: 15px; align-items: center; }
@media (min-width: 400px) { .converter-form { grid-template-columns: 1fr auto 1fr; } }
.converter-form input, .converter-form select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 1rem; }
.swap-icon { text-align: center; }
.converter-result { margin-top: 20px; text-align: center; }
.converter-result p { margin: 0; color: #6c757d; }
.converter-result strong { font-size: 1.8rem; color: var(--primary-color); }
</style>