import {createApp} from 'vue';
import './style.css';
import App from './App.vue';
import components from './components/UI';
import GoogleSignInPlugin from "vue3-google-signin"
import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap/dist/js/bootstrap.js";
import 'mdb-vue-ui-kit/css/mdb.min.css'
import axios from "axios";
import VueAxios from "vue-axios";



const app = createApp(App)

const gauthOption = {
    clientId: import.meta.env.VITE_GOOGLE_KEY
}
app.use(GoogleSignInPlugin, gauthOption)
axios.defaults.baseURL = 'http://localhost:8000/backend/api/'

app.use(VueAxios, axios)
components.forEach(component => {
    app.component(component.name, component)
})


app.mount('#app')

