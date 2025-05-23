import axios from 'axios'
import { createStore } from 'vuex'

// Optionnel : on peut extraire baseURL dans un fichier api.js
const API_BASE = 'http://localhost:8000'

export const sitesModule = {
  namespaced: true,
  state: () => ({
    sites: []
  }),
  mutations: {
    SET_SITES(state, sites) {
      state.sites = sites
    },
    ADD_SITE(state, site) {
      state.sites.push(site)
    },
    UPDATE_SITE(state, updated) {
      const idx = state.sites.findIndex(s => s.id === updated.id)
      if (idx !== -1) state.sites.splice(idx, 1, updated)
    },
    DELETE_SITE(state, id) {
      state.sites = state.sites.filter(s => s.id !== id)
    }
  },
  actions: {
    async fetchSites({ commit }) {
      try {
        const res = await axios.get(`${API_BASE}/sites/`)
        commit('SET_SITES', res.data)
      } catch (error) {
        console.error('Erreur fetchSites:', error)
      }
    },
    async addSite({ commit }, payload) {
      try {
        const res = await axios.post(`${API_BASE}/sites/`, payload)
        commit('ADD_SITE', res.data)
        return res.data
      } catch (error) {
        console.error('Erreur addSite:', error)
      }
    },
    async updateSite({ commit }, { id, payload }) {
      try {
        const res = await axios.put(`${API_BASE}/sites/${id}`, payload)
        commit('UPDATE_SITE', res.data)
        return res.data
      } catch (error) {
        console.error('Erreur updateSite:', error)
      }
    },
    async deleteSite({ commit }, id) {
      try {
        await axios.delete(`${API_BASE}/sites/${id}`)
        commit('DELETE_SITE', id)
      } catch (error) {
        console.error('Erreur deleteSite:', error)
      }
    }
  }
}

export default createStore({
  modules: { sites: sitesModule }
})
