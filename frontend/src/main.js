import {createApp} from 'vue';
import App from './App.vue';
import components from './components/UI';
import GoogleSignInPlugin from "vue3-google-signin"
import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap/dist/js/bootstrap.js";
import 'mdb-vue-ui-kit/css/mdb.min.css'
import axios from "axios";
import VueAxios from "vue-axios";
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import {useVuelidate} from '@vuelidate/core'
import router from './router'
import vuetify from './plugins/vuetify'
import {loadFonts} from './plugins/webfontloader'
import store from './store'

loadFonts()


const app = createApp(App)

const gauthOption = {
    clientId: import.meta.env.VITE_GOOGLE_KEY
}
app.use(GoogleSignInPlugin, gauthOption)
axios.defaults.baseURL = 'http://localhost/backend/api/'
app.use(store)
app.use(VueAxios, axios)
app.use(router)
app.use(useVuelidate)
app.use(vuetify, {
    iconfont: 'md'
})
components.forEach(component => {
    app.component(component.name, component)
})


app.mount('#app')
