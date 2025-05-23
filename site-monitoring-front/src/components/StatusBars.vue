<template>
    <div class="status-bars">
      <div
        v-for="(bar, index) in bars"
        :key="index"
        :class="['bar', colorClass(bar)]"
      />
    </div>
  </template>
  
  <script setup>
  import { ref, watch, defineProps } from 'vue'
  
  const props = defineProps({
    /**
     * Nombre de cases à afficher.
     */
    count: {
      type: Number,
      default: 15
    },
    /**
     * Flux de métriques (array d'objets contenant au moins `up` et `status_code`).
     */
    statuses: {
      type: Array,
      default: () => []
    }
  })
  
  // Tableau circulaire des cases
  const bars = ref(Array(props.count).fill(null))
  const pointer = ref(0)
  
  // Met à jour le ring buffer à chaque nouvel élément dans `statuses`
  watch(
    () => props.statuses.length,
    (newLen, oldLen) => {
      if (newLen === 0) {
        // Reset du buffer quand on change de site
        bars.value = Array(props.count).fill(null)
        pointer.value = 0
      } else if (newLen > oldLen) {
        const latest = props.statuses[newLen - 1]
        bars.value[pointer.value] = latest
        pointer.value = (pointer.value + 1) % props.count
      }
    }
  )
  
  /**
   * Détermine la classe de couleur selon le statut.
   */
  function colorClass(status) {
    if (!status) return 'empty'
    if (status.up) return 'green'
    // erreurs HTTP 4xx -> orange, autres erreurs -> red
    if (status.status_code >= 400 && status.status_code < 500) return 'orange'
    return 'red'
  }
  </script>
  
  <style scoped>
  .status-bars {
    display: flex;
    gap: 2px;
  }
  .bar {
    flex: 1;
    height: 8px;
    background: #eee;
    border-radius: 2px;
  }
  .bar.green {
    background: #4caf50;
  }
  .bar.orange {
    background: #fb8c00;
  }
  .bar.red {
    background: #f44336;
  }
  .bar.empty {
    background: #ddd;
  }
  </style>
  