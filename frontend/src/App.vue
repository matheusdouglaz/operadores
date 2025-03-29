<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-app-bar-title>Sistema de Busca de Operadoras</v-app-bar-title>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-card>
              <v-card-title class="text-h5">
                Busca de Operadoras
              </v-card-title>
              
              <v-card-text>
                <v-text-field
                  v-model="searchQuery"
                  label="Digite para buscar..."
                  prepend-icon="mdi-magnify"
                  @input="searchOperadoras"
                  clearable
                  variant="outlined"
                  full-width
                  hide-details
                ></v-text-field>
              </v-card-text>

              <v-card-text>
                <v-progress-circular
                  v-if="loading"
                  indeterminate
                  color="primary"
                ></v-progress-circular>

                <v-alert
                  v-if="error"
                  type="error"
                  dismissible
                >
                  {{ error }}
                </v-alert>

                <v-data-table
                  v-if="operadoras.length > 0"
                  :headers="headers"
                  :items="operadoras"
                  :loading="loading"
                  class="elevation-1"
                >
                  <template v-slot:item.actions="{ item }">
                    <v-btn
                      size="small"
                      color="primary"
                      @click="showDetails(item)"
                    >
                      Detalhes
                    </v-btn>
                  </template>
                </v-data-table>

                <v-alert
                  v-else-if="!loading && !error"
                  type="info"
                >
                  Nenhuma operadora encontrada
                </v-alert>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Detalhes da Operadora</span>
        </v-card-title>
        
        <v-card-text v-if="selectedOperadora">
          <v-row>
            <v-col cols="6">
              <strong>Razão Social:</strong> {{ selectedOperadora.razao_social }}
            </v-col>
            <v-col cols="6">
              <strong>Nome Fantasia:</strong> {{ selectedOperadora.nome_fantasia }}
            </v-col>
            <v-col cols="6">
              <strong>CNPJ:</strong> {{ selectedOperadora.cnpj }}
            </v-col>
            <v-col cols="6">
              <strong>Modalidade:</strong> {{ selectedOperadora.modalidade }}
            </v-col>
          </v-row>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="dialog = false">Fechar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data: () => ({
    searchQuery: '',
    operadoras: [],
    loading: false,
    error: null,
    dialog: false,
    selectedOperadora: null,
    headers: [
      { title: 'Razão Social', key: 'razao_social' },
      { title: 'Nome Fantasia', key: 'nome_fantasia' },
      { title: 'CNPJ', key: 'cnpj' },
      { title: 'Modalidade', key: 'modalidade' },
      { title: 'Ações', key: 'actions', sortable: false }
    ]
  }),
  methods: {
    async searchOperadoras() {
      if (!this.searchQuery) {
        this.operadoras = []
        return
      }
      
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get(`http://127.0.0.1:5000/operadoras/busca?q=${this.searchQuery}`)
        this.operadoras = response.data
      } catch (err) {
        this.error = 'Erro ao buscar operadoras. Por favor, tente novamente.'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    
    showDetails(operadora) {
      this.selectedOperadora = operadora
      this.dialog = true
    }
  }
}
</script>

<style>
.v-application {
  font-family: 'Roboto', sans-serif;
}
</style> 