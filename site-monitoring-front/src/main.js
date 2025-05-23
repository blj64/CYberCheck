import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

import sites from './store/sites'

createApp(App)
  .use(sites)
  .mount('#app')