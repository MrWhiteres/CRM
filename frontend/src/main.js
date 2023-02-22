import {createApp} from 'vue';
import './style.css';
import App from './App.vue';
import components from './components/UI';
import vue3GoogleLogin from 'vue3-google-login'
import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap/dist/js/bootstrap.js";
import 'mdb-vue-ui-kit/css/mdb.min.css'


const app = createApp(App)

const gauthOption = {
    clientId: import.meta.env.VITE_GOOGLE_KEY,
}
app.use(vue3GoogleLogin, gauthOption)
components.forEach(component => {
    app.component(component.name, component)
})


app.mount('#app')

