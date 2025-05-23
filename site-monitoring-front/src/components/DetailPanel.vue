<template>
  <div class="detail-panel">
    <div class="actions">
      <button class="edit-button" @click="onEdit">Edit Website</button>
      <button class="delete-button" @click="onDelete">Delete Website</button>
      <button class="clear-button" @click="onClear">Clear Logs</button>
    </div>
    <h2>{{ site.name }}</h2>
    <StatusBars :count="15" :statuses="metricsList" />

    <div class="status-header">
      <!-- Up/Down indicator icon -->
      <div class="status-indicator" :class="{ up: latestUp, down: !latestUp }">
        <span v-if="latestUp">✔︎ Up</span>
        <span v-else>✖︎ Down</span>
      </div>
    </div>

    <!-- Info summary box -->
    <div class="info-box">
      <div class="info-item">
        <div class="info-label">Response (Current)</div>
        <div class="info-value">{{ latestResponseTime }} ms</div>
      </div>
      <div class="info-item">
        <div class="info-label">Avg. Response (24h)</div>
        <div class="info-value">{{ avg24h }} ms</div>
      </div>
      <div class="info-item">
        <div class="info-label">Uptime (24h)</div>
        <div class="info-value">{{ uptime24h }}%</div>
      </div>
      <div class="info-item">
        <div class="info-label">Cert Expiry (days)</div>
        <div class="info-value">{{ certExpiryDays }}</div>
      </div>
      <div class="info-item">
        <div class="info-label">TLS Version</div>
        <div class="info-value">{{ latestEntry.tls_version || '–' }}</div>
      </div>
      <div class="info-item">
        <div class="info-label">Cipher Suite</div>
        <div class="info-value">{{ latestEntry.cipher_suite || '–' }}</div>
      </div>
      <div class="info-item">
        <div class="info-label">Mixed Content</div>
        <div class="info-value">
          <span v-if="latestEntry.mixed_content">⚠️ Yes</span>
          <span v-else>–</span>
        </div>
      </div>
    </div>
    
    <div class="chart-container">
      <canvas ref="msCanvas"></canvas>
    </div>

    <div class="metrics">
      <h3>Live Metrics</h3>
      <table v-if="metricsList.length > 0">
        <thead>
          <tr>
            <th>Site</th>
            <th>Heure</th>
            <th>HTTP</th>
            <th>Resp (ms)</th>
            <th>Ping (ms)</th>
            <th>DNS (ms)</th>
            <th>TLS (ms)</th>
            <th>Expire Cert</th>
            <th>Erreur</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in metricsList" :key="m.timestamp">
            <td>{{ site.name }}</td>
            <td>{{ new Date(m.timestamp).toLocaleTimeString() }}</td>
            <td>{{ m.status_code }}</td>
            <td>{{ m.response_time_ms }}</td>
            <td>{{ m.ping_ms }}</td>
            <td>{{ m.dns_ms }}</td>
            <td>{{ m.tls_handshake_ms }}</td>
            <td>{{ m.cert_expires_at ? new Date(m.cert_expires_at).toLocaleString() : '–' }}</td>
            <td>{{ m.error_message || '–' }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else>
        En attente des premières métriques…
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, watch, computed } from 'vue'
import { defineProps, defineEmits } from 'vue'
import axios from 'axios'
import { Chart, registerables } from 'chart.js'
import StatusBars from './StatusBars.vue'
Chart.register(...registerables)

const props = defineProps({ site: { type: Object, required: true } })
const emit = defineEmits(['edit-website', 'delete-website'])

const metricsList = ref([])
let ws = null
const msCanvas = ref(null)
let msChart = null

// Computed for indicator and summary
const latestEntry = computed(() => metricsList.value[0] || {})
const latestUp = computed(() => latestEntry.value.up)
const latestResponseTime = computed(() => latestEntry.value.response_time_ms || '-')

// Placeholder computations; implement actual logic
const avg24h = computed(() => {
  const slice = metricsList.value.slice(0, 72)
  const times = slice.map(m => m.response_time_ms).filter(Boolean)
  if (!times.length) return '-'
  return Math.round(times.reduce((a,b)=>a+b,0)/times.length)
})
const uptime24h = computed(() => {
  const slice = metricsList.value.slice(0, 72)
  if (!slice.length) return '-'
  const upCount = slice.filter(m => m.up).length
  return Math.round((upCount / slice.length) * 100)
})
const certExpiryDays = computed(() => {
  const expires = latestEntry.value.cert_expires_at
  if (!expires) return '-'
  const diff = (new Date(expires) - new Date())/86400000
  return Math.round(diff)
})


// Charge les 10 dernières métriques
async function loadInitialMetrics() {
  try {
    const res = await axios.get(
      `http://localhost:8000/sites/${props.site.id}/checks/`,
      { params: { limit: 10 } }
    )
    metricsList.value = res.data
    updateChart()
  } catch (e) {
    console.error('Erreur chargement historiques :', e)
    metricsList.value = []
  }
}

// Initialise le graphique
function initChart() {
  const ctx = msCanvas.value.getContext('2d')
  msChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{ label: 'Response Time (ms)', data: [], fill: false, tension: 0.1 }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { display: true, title: { display: true, text: 'Heure' } },
        y: { display: true, title: { display: true, text: 'ms' } }
      }
    }
  })
}

// Met à jour le graphique
function updateChart() {
  if (!msChart) return
  const slice = metricsList.value.slice(0, 20).reverse()
  msChart.data.labels = slice.map(m => new Date(m.timestamp).toLocaleTimeString())
  msChart.data.datasets[0].data = slice.map(m => m.response_time_ms)
  msChart.update()
}

// Surveillance WS et historique
watch(
  () => props.site.id,
  async () => {
    // Réinit
    metricsList.value = []
    if (ws) ws.close()

    // Historique + Chart
    await loadInitialMetrics()
    initChart()

    // WebSocket
    ws = new WebSocket('ws://localhost:8000/ws')
    ws.onmessage = event => {
      const data = JSON.parse(event.data)
      if (data.site_id === props.site.id) {
        metricsList.value.unshift(data)
        if (metricsList.value.length > 50) metricsList.value.pop()
        updateChart()
      }
    }
  },
  { immediate: true }
)

onUnmounted(() => {
  if (ws) ws.close()
  if (msChart) msChart.destroy()
})

// Émetteurs d'événements
function onEdit() {
  emit('edit-website', props.site)
}
function onDelete() {
  emit('delete-website', props.site)
}

// Clear logs
async function onClear() {
  try {
    await axios.delete(`http://localhost:8000/sites/${props.site.id}/checks/`)
    metricsList.value = []
    if (msChart) {
      msChart.data.labels = []
      msChart.data.datasets[0].data = []
      msChart.update()
    }
  } catch (e) {
    console.error('Erreur clear logs :', e)
  }
}
</script>

<style scoped>
.detail-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.actions {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.edit-button,
.delete-button,
.clear-button {
  padding: 0.3rem 0.6rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.edit-button {
  background: #ffc107;
  color: #000;
}
.delete-button {
  background: #f44336;
  color: #fff;
}
.clear-button {
  background: #6c757d;
  color: #fff;
}
.chart-container {
  width: 100%;
  height: 400px; /* agrandi à 400px */
  margin-bottom: 1rem;
  position: relative;
}
.chart-container canvas {
  width: 100% !important;
  height: 100% !important;
}
.metrics {
  flex: 1;
  overflow-y: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 0.3rem 0.5rem;
  border: 1px solid #ddd;
  text-align: center;
}
thead {
  background: #f0f0f0;
}
.error-bg {
  background-color: #f8d7da;
}
.success-bg {
  background-color: #d4edda;
}

.status-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.status-indicator {
  font-size: 1.2rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  color: #fff;
}
.status-indicator.up { background-color: #4caf50 }
.status-indicator.down { background-color: #f44336 }

.info-box {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  background: #222;
  padding: 1rem;
  border-radius: 8px;
}
.info-item {
  text-align: center;
  color: #fff;
}
.info-label { font-size: 0.8rem; color: #aaa }
.info-value { font-size: 1.2rem; }

</style>
