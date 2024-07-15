// import './assets/main.css'
import './assets/reset.css'
import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';
import VueAxios from 'vue-axios';

const app = createApp(App);
axios.defaults.baseURL = 'http://127.0.0.1:8000'; // Reemplaza con la URL base de tu API


app.use(VueAxios, axios);

app.mount('#app');

createApp(App).mount('#app')
