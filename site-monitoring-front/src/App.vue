<template>
  
  <div class="container">
    <!-- Left panel for listing sites and adding new ones -->
    <LeftPanel
      @site-selected="onSelect"
      @add-website="onAdd"
    />

    <!-- Right panel: show Add, Edit or Details based on state -->
    <div class="right-panel">
      <!-- Add form -->
      <RightPanel
        v-if="mode === 'add'"
        @saved="onSaved"
        @cancel="mode = 'view'"
      />

      <!-- Edit form -->
      <EditPanel
        v-else-if="mode === 'edit' && selectedSite"
        :site="selectedSite"
        @updated="onUpdated"
        @cancel="mode = 'view'"
      />

      <!-- Detail view -->
      <DetailPanel
        v-else-if="mode === 'view' && selectedSite"
        :site="selectedSite"
        @edit-website="onEdit"
        @delete-website="onDelete"
      />

      <!-- Placeholder if nothing selected/add/edit -->
      <div v-else class="placeholder">
        Sélectionne un site à gauche ou ajoute-en un nouveau.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from 'vuex'
import LeftPanel from './components/LeftPanel.vue'
import RightPanel from './components/RightPanel.vue'
import EditPanel from './components/EditPanel.vue'
import DetailPanel from './components/DetailPanel.vue'

const store = useStore()
const selectedSite = ref(null)
// mode can be 'view', 'add', 'edit'
const mode = ref('view')

function onSelect(site) {
  selectedSite.value = site
  mode.value = 'view'
}

function onAdd() {
  selectedSite.value = null
  mode.value = 'add'
}

// After creating a site
function onSaved(newSite) {
  store.dispatch('sites/fetchSites')
  selectedSite.value = newSite
  mode.value = 'view'
}

// When clicking Edit in DetailPanel
function onEdit(site) {
  selectedSite.value = site
  mode.value = 'edit'
}

// After editing
function onUpdated(updatedSite) {
  store.dispatch('sites/fetchSites')
  selectedSite.value = updatedSite
  mode.value = 'view'
}

// When clicking Delete in DetailPanel
async function onDelete(site) {
  if (confirm(`Supprimer le site « ${site.name} » ?`)) {
    await store.dispatch('sites/deleteSite', site.id)
    selectedSite.value = null
    mode.value = 'view'
  }
}
</script>

<style>
.container { display: flex; height: 100vh; }
.right-panel { flex: 1; display: flex; flex-direction: column; }
.placeholder { padding: 1rem; color: #666; }
</style>
