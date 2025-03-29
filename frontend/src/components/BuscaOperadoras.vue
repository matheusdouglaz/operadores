<template>
  <div class="busca-operadoras">
    <h2>Busca de Operadoras</h2>
    
    <div class="search-box">
      <input 
        v-model="termoBusca" 
        @input="buscarOperadoras" 
        placeholder="Digite para buscar..."
        class="search-input"
      >
    </div>

    <div v-if="carregando" class="loading">
      Carregando...
    </div>

    <div v-else-if="erro" class="error">
      {{ erro }}
    </div>

    <div v-else class="resultados">
      <div v-if="operadoras.length === 0" class="sem-resultados">
        Nenhuma operadora encontrada
      </div>
      
      <div v-else class="operadoras-grid">
        <div v-for="operadora in operadoras" :key="operadora.cnpj" class="operadora-card">
          <h3>{{ operadora.razao_social }}</h3>
          <p><strong>CNPJ:</strong> {{ operadora.cnpj }}</p>
          <p><strong>Nome Fantasia:</strong> {{ operadora.nome_fantasia }}</p>
          <p><strong>Modalidade:</strong> {{ operadora.modalidade }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BuscaOperadoras',
  data() {
    return {
      termoBusca: '',
      operadoras: [],
      carregando: false,
      erro: null
    }
  },
  methods: {
    async buscarOperadoras() {
      if (!this.termoBusca) {
        this.operadoras = []
        return
      }

      this.carregando = true
      this.erro = null

      try {
        const response = await fetch(`http://127.0.0.1:5000/operadoras/busca?q=${encodeURIComponent(this.termoBusca)}`)
        if (!response.ok) {
          throw new Error('Erro ao buscar operadoras')
        }
        this.operadoras = await response.json()
      } catch (error) {
        this.erro = error.message
        this.operadoras = []
      } finally {
        this.carregando = false
      }
    }
  }
}
</script>

<style scoped>
.busca-operadoras {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.search-box {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.loading, .error, .sem-resultados {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

.error {
  color: red;
}

.operadoras-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.operadora-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.operadora-card h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.operadora-card p {
  margin: 5px 0;
  color: #666;
}

.operadora-card strong {
  color: #333;
}
</style> 