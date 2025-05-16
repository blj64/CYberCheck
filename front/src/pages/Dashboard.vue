<template>
    <div class="dashboard">
      <Header />
      <div class="main-layout">
        <LeftPanel class="left" @select-website="fetchWebsiteDetailsHandler" />
        <RightPanel class="right" :selected-website="selectedWebsite" :show-form="showForm" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, provide } from 'vue'
  import Header from '../components/Header.vue'
  import LeftPanel from '../components/LeftPanel.vue'
  import RightPanel from '../components/RightPanel.vue'
  import { fetchWebsiteDetails } from '../store/websites.js' // Import the correct function

  const showForm = ref(false) // Shared state for showing the form
  const selectedWebsite = ref(null) // State for the selected website

  function toggleForm() {
    showForm.value = !showForm.value
  }

  async function fetchWebsiteDetailsHandler(id) {
    console.log(`Fetching details for website ID: ${id}`) // Debug log
    try {
      showForm.value = false // Hide the form when selecting a website
      selectedWebsite.value = await fetchWebsiteDetails(id) // Update selected website
      console.log('Website details fetched:', selectedWebsite.value) // Log the fetched details
    } catch (error) {
      console.error('Error fetching website details:', error) // Log any errors
    }
  }

  provide('toggleForm', toggleForm) // Provide the toggleForm function
  provide('showForm', showForm) // Provide the shared state
  </script>
  
  <style scoped>
  .dashboard {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }
  
  .main-layout {
    display: flex;
    flex: 1;
    height: 100%;
  }
  
  .left {
    width: 30%;
  }
  
  .right {
    width: 70%;
    overflow-y: auto;
  }
  </style>
