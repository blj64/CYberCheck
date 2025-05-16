import { reactive } from 'vue'
import axios from 'axios'

export function useWebsiteStore() {
  const state = reactive({
    websites: [], // Reactive state for websites
  })

  async function fetchWebsites() {
    const res = await axios.get('http://localhost:8000/websites')
    state.websites.splice(0, state.websites.length, ...res.data) // Update the array reactively
  }

  async function addWebsite(data) {
    await axios.post('http://localhost:8000/websites', data)
    await fetchWebsites() // Fetch the updated list of websites
  }

  async function fetchWebsiteDetails(id) {
    const res = await axios.get(`http://localhost:8000/websites/${id}/details`)
    return res.data
  }

  return {
    state,
    fetchWebsites,
    addWebsite,
    fetchWebsiteDetails, // Expose the new method
  }
}
