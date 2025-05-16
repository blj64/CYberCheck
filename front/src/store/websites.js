import { ref } from 'vue'

export const websites = ref([])

export async function fetchWebsites() {
  try {
    const res = await fetch('http://localhost:8000/websites')
    websites.value = await res.json()
  } catch (error) {
    console.error('Error fetching websites:', error)
  }
}

export async function fetchWebsiteDetails(id) {
  try {
    const res = await fetch(`http://localhost:8000/websites/${id}/details`)
    return await res.json()
  } catch (error) {
    console.error('Error fetching website details:', error)
    throw error
  }
}

export async function addWebsite(website) {
  try {
    const response = await fetch('http://localhost:8000/websites/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(website), // Ensure the data matches the schema
    })
    if (!response.ok) {
      throw new Error('Failed to add website')
    }
    const newWebsite = await response.json()
    websites.value.push(newWebsite) // Add the new website to the state
  } catch (error) {
    console.error('Error adding website:', error)
    throw error
  }
}
