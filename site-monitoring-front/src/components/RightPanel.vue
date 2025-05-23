<template>
    <div class="right-panel">
      <h2>Add a new site</h2>
      <form @submit.prevent="onSubmit">
        <label>
          Name
          <input v-model="name" required />
        </label>
        <label>
          URL
          <input v-model="url" type="url" required />
        </label>
        <label>
          Delay (seconds)
          <input v-model.number="delay" type="number" min="1" required />
        </label>
        <div class="buttons">
          <button type="submit">Save</button>
          <button type="button" @click="onCancel">Cancel</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useStore } from 'vuex'
  
  const store = useStore()
  
  // champs du formulaire
  const name = ref('')
  const url = ref('')
  const delay = ref(60)
  
  // événements vers le parent
  const emit = defineEmits(['saved','cancel'])
  
  async function onSubmit() {
    await store.dispatch('sites/addSite', {
      name: name.value,
      url: url.value,
      delay_seconds: delay.value
    })
    emit('saved')
  }
  
  function onCancel() {
    emit('cancel')
  }
  </script>
  
  <style scoped>
  .right-panel {
    padding: 1rem;
  }
  label {
    display: block;
    margin-bottom: 0.5rem;
  }
  input {
    width: 100%;
    padding: 0.3rem;
    margin-top: 0.2rem;
    box-sizing: border-box;
  }
  .buttons {
    margin-top: 1rem;
  }
  button {
    margin-right: 0.5rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  button[type="submit"] {
    background: #2196f3;
    color: white;
  }
  button[type="button"] {
    background: #f44336;
    color: white;
  }
  </style>
  