<template>
  <aside class="left-panel">
    <p>Left Panel</p>
    <button class="add-button" @click="toggleForm">Add Website</button>
    <div v-for="website in websites" :key="website.id">
      <button
        class="website-button"
        :class="website.status"
        @click="$emit('select-website', website.id); console.log('Selected website ID:', website.id)"
      >
        {{ website.name }}
      </button>
    </div>
  </aside>
</template>

<script setup>
import { onMounted, inject } from 'vue'
import { websites, fetchWebsites } from '../store/websites.js'

const toggleForm = inject('toggleForm') // Inject the toggleForm function

onMounted(() => {
  fetchWebsites() // Fetch websites when the component is mounted
})
</script>

<style scoped>
.left-panel {
  background-color: #2196F3; /* bleu */
  color: white;
  padding: 10px;
  height: 100%;
}

.website-button.up {
  background-color: #e8f5e9; /* vert clair */
  color: #2e7d32;            /* vert foncé */
}

.website-button.up:hover {
  background-color: #c8e6c9;
  color: #1b5e20;
}

.website-button.down {
  background-color: #ffebee; /* rouge clair */
  color: #c62828;            /* rouge foncé */
}

.website-button.down:hover {
  background-color: #ffcdd2;
  color: #b71c1c;
}

.website-button.unknown {
  background-color: #fffde7; /* jaune clair */
  color: #f9a825;            /* jaune foncé */
}

.website-button.unknown:hover {
  background-color: #fff59d;
  color: #f57f17;
}


.add-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 5px 10px;
  margin-bottom: 10px;
  cursor: pointer;
  border-radius: 4px;
}

.add-button:hover {
  background-color: #45A049;
}
</style>
