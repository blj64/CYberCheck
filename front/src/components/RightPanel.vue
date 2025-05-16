<template>
  <aside class="right-panel">
    <p>Right Panel</p>
    <div v-if="selectedWebsite">
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
    </div>
    <div v-else>
      <p>Select a website to view its details.</p>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  selectedWebsite: Object, // Ensure this matches the prop name in Dashboard.vue
})
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