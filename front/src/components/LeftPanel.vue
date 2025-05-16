<template>
  <aside class="left-panel">
    <p>Left Panel</p>
    <button class="add-button" @click="toggleForm">Add Website</button>
    <div v-for="website in store.state.websites" :key="website.id">
      <button
        class="website-button"
        @click="$emit('select-website', website.id); console.log('Selected website ID:', website.id)"
      >
        {{ website.name }}
      </button>
    </div>
  </aside>
</template>

<script setup>
import { onMounted, inject } from 'vue'
import { useWebsiteStore } from '../store/websites.js'

const store = useWebsiteStore()
const toggleForm = inject('toggleForm') // Inject the toggleForm function

onMounted(() => {
  store.fetchWebsites() // Fetch websites when the component is mounted
})
</script>

<style scoped>
.left-panel {
  background-color: #2196F3; /* bleu */
  color: white;
  padding: 10px;
  height: 100%;
}

.website-button {
  background-color: white;
  color: #2196F3;
  border: none;
  padding: 5px 10px;
  margin: 5px 0;
  cursor: pointer;
  border-radius: 4px;
}

.website-button:hover {
  background-color: #1976D2;
  color: white;
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
