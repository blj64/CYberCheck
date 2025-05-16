<template>
  <aside class="right-panel">
    <p>Right Panel</p>
    <div v-if="showForm">
      <h2>Add a New Website</h2>
      <form @submit.prevent="addWebsiteHandler">
        <input v-model="newWebsite.name" placeholder="Website Name" required />
        <input v-model="newWebsite.url" placeholder="Website URL" required />
        <input v-model.number="newWebsite.interval" placeholder="Check Interval (minutes)" required />
        <button type="submit" class="add-button">Submit</button>
      </form>
    </div>
    <div v-else-if="selectedWebsite">
      <h2>{{ selectedWebsite.website.name }}</h2>
      <p>{{ selectedWebsite.website.url }}</p>
      <div v-if="selectedWebsite.latest_check_result">
        <h3>Latest Check Result:</h3>
        <ul>
          <li>Status Code: {{ selectedWebsite.latest_check_result.status_code }}</li>
          <li>Ping: {{ selectedWebsite.latest_check_result.ping }}ms</li>
          <li>Checked At: {{ selectedWebsite.latest_check_result.checked_at }}</li>
        </ul>
      </div>
      <div v-else>
        <p>No check results available for this website.</p>
      </div>
      <div v-if="selectedWebsite.recent_check_results && selectedWebsite.recent_check_results.length">
        <h3>Recent Check Results:</h3>
        <ul>
          <li v-for="result in selectedWebsite.recent_check_results" :key="result.checked_at">
            <strong>{{ result.checked_at }}:</strong> Status Code: {{ result.status_code }}, Ping: {{ result.ping }}ms
          </li>
        </ul>
      </div>
    </div>
    <div v-else>
      <p>Select a website to view its details.</p>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { addWebsite } from '../store/websites.js'

defineProps({
  selectedWebsite: Object,
  showForm: Boolean, // New prop to control form visibility
})

const newWebsite = ref({ name: '', url: '', interval: 5 }) // Default interval value

async function addWebsiteHandler() {
  try {
    console.log('Adding website:', newWebsite.value)
    await addWebsite(newWebsite.value) // Call the function to add the website
    newWebsite.value = { name: '', url: '', interval: 5 } // Reset the form
    alert('Website added successfully!')
  } catch (error) {
    console.error('Error adding website:', error)
    alert('Failed to add website.')
  }
}
</script>

<style scoped>
.right-panel {
  background-color: #f44336; /* rouge */
  color: white;
  padding: 10px;
  height: 100%;
}

form {
  margin-top: 20px;
}

input {
  display: block;
  margin: 5px 0;
  padding: 5px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.add-button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 4px;
}

.add-button:hover {
  background-color: #45A049;
}
</style>