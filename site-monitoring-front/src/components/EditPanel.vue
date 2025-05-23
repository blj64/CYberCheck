<template>
    <div class="edit-panel">
      <h2>Edit Website</h2>
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
          <input v-model.number="delaySeconds" type="number" min="1" required />
        </label>
        <div class="buttons">
          <button type="submit">Save</button>
          <button type="button" @click="onCancel">Cancel</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useStore } from 'vuex'
  import { defineProps, defineEmits } from 'vue'
  
  const props = defineProps({
    site: { type: Object, required: true }
  })
  const emit = defineEmits(['updated', 'cancel'])
  const store = useStore()
  
  // Form fields
  const name = ref('')
  const url = ref('')
  const delaySeconds = ref(0)
  
  // Initialize form with current site data
  onMounted(() => {
    name.value = props.site.name
    url.value = props.site.url
    delaySeconds.value = props.site.delay_seconds || props.site.delaySeconds || 60
  })
  
  async function onSubmit() {
    const payload = {
      name: name.value,
      url: url.value,
      delay_seconds: delaySeconds.value
    }
    const updated = await store.dispatch('sites/updateSite', { id: props.site.id, payload })
    if (updated) {
      emit('updated', updated)
    }
  }
  
  function onCancel() {
    emit('cancel')
  }
  </script>
  
  <style scoped>
  .edit-panel {
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
  