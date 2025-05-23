<template>
    <div class="left-panel">
      <h2>Sites monitorés</h2>
      <button class="add-button" @click="onAdd">
      + Add Website
    </button>
      <div v-if="sites.length === 0">
        Chargement…
      </div>
      <div v-else>
        <div
          v-for="site in sites"
          :key="site.id"
          class="site-row"
          @click="selectSite(site)"
        >
        <button class="site-button">
          {{ site.name }}
        </button>
        <!-- Les 5 cases dynamiques pour CE site -->
        <StatusBars :count="5" :statuses="statusesBySite[site.id] || []" />
      </div>

      </div>
    </div>
  </template>
  
  <script setup>
  import { computed, onMounted, reactive, onUnmounted } from 'vue'
  import { useStore } from 'vuex'
  import StatusBars from './StatusBars.vue'
  // Récupère le store Vuex
  const store = useStore()
  
  // Calcule la liste des sites à partir du state 'sites' du module 'sites'
  const sites = computed(() => store.state.sites.sites)
  const statusesBySite = reactive({})  // { [site_id]: [metrics, ...] }

  let ws = null
  onMounted(() => {
    // Charger la liste si besoin
    store.dispatch('sites/fetchSites')

    // Ouvrir la WS
    ws = new WebSocket('ws://localhost:8000/ws')
    ws.onmessage = evt => {
      const m = JSON.parse(evt.data)
      // Prépare le tableau pour ce site s’il n’existe pas
      if (!statusesBySite[m.site_id]) {
        statusesBySite[m.site_id] = []
      }
      // Insertion en ring buffer
      statusesBySite[m.site_id].unshift(m)
      if (statusesBySite[m.site_id].length > 5) {
        statusesBySite[m.site_id].pop()
      }
    }
  })
  // Émet l'événement 'site-selected'
  const emit = defineEmits(['site-selected', 'add-website'])
  function selectSite(site) {
    emit('site-selected', site)
  }
  function onAdd() {
    emit('add-website')
  }
  </script>
  
  <style scoped>
  .left-panel {
    padding: 1rem;
    border-right: 1px solid #ddd;
  }
  .site-button {
    display: block;
    width: 100%;
    margin-bottom: 0.5rem;
    padding: 0.5rem;
    text-align: left;
    background: #20ae1e;
    border: none;
    cursor: pointer;
    border-radius: 4px;
  }
  .site-button:hover {
    background: #147813;
  }

  .add-button {
  margin-top: 1rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  width: 100%;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.add-button:hover {
  background: #45a049;
}
  </style>
  