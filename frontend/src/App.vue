<template>
    <v-app>
        <nav-bar/>
        <v-main>
            <router-view/>
        </v-main>
        <footer-component/>
    </v-app>
</template>

<script>

import NavBar from "./components/NavBar.vue";
import FooterComponent from "./components/FooterComponent.vue";
import {watchEffect} from "vue";
import axios from "axios";
import {useStore} from 'vuex'

export default {
    name: 'App',
    components: {FooterComponent, NavBar},
    beforeCreate() {
    },
    setup() {
        const store = useStore();
        store.dispatch('initializeStore');
        watchEffect(() => {
            axios.defaults.headers['Authorization'] = `Bearer ${store.state.access}`;
        });
    },
    mounted() {
        if (!this.$store.state.access && localStorage.getItem('refresh')) {
            this.restoreAccess()
        }
    },
    methods: {
        restoreAccess() {
            axios
                .post('refresh_token/', {refresh: localStorage.getItem('refresh')})
                .then(response => {
                    this.$store.commit('setAccess', response.data.access)
                })
                .catch(

                )
        }
    }
}
</script>


