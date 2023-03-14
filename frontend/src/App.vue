<template>
  <v-app>
    <div>
      <div v-if="loading" class="loader-container">
        <div class="loader-inner">
          <v-progress-circular :size="64" :width="7" color="primary" indeterminate></v-progress-circular>
        </div>
      </div>
      <div v-else>
        <nav-bar/>
        <v-main class="md-5 mt-5">
          <router-view/>
        </v-main>
        <footer-component/>
      </div>
    </div>


  </v-app>
</template>

<script>

import NavBar from "./components/NavBar.vue";
import FooterComponent from "./components/FooterComponent.vue";
import {ref, watchEffect} from "vue";
import axios from "axios";
import {useStore} from 'vuex'
import {useRouter} from "vue-router";

export default {
  name: 'App',
  components: {FooterComponent, NavBar},
  setup() {
    const store = useStore();
    store.dispatch('initializeStore');
    const router = useRouter();

    if (window.location.pathname.includes('/confirm_email/') && !store.state.user) {
    } else {
      if (window.location.pathname.includes('/confirm_email/') && store.state.user) {
        router.push({name: 'profile'});
      } else {
        if ('auth/' !== router.currentRoute.value.fullPath && !store.state.user) {
          router.push({name: 'auth'});
        }
      }
    }
    watchEffect(() => {
      axios.defaults.headers['Authorization'] = store.state.access.length ? `Bearer ${store.state.access}` : ''
    });


    const getUserProfile = async () => {
      axios.defaults.headers['Authorization'] = `Bearer ${store.state.access}`
      try {
        const response = await axios.get('/user/profile')
        let image = response.data.image
        if (image) {
          try {
            const responseImage = await axios.get('user/image/', {responseType: 'blob'})
            response.data.image = URL.createObjectURL(new Blob([responseImage.data], {type: 'text/plain;charset=utf-8'}))
          } catch (_) {}
        }
        store.commit('setUser', response.data)
      } catch (error) {
        if (error.response.data.code === 'user_not_found') {
          localStorage.clear()
          store.commit('clearState')
          await router.push({name: 'auth'})
        }
      }
    }

    setInterval(() => {
      if (store.state.access && !store.state.user) {
        getUserProfile()
      }
    }, 1_000)

    const restoreAccess = async () => {
      delete axios.defaults.headers['Authorization']
      try {
        const response = await axios.post('refresh_token/', {refresh: store.state.refresh})
        store.commit('setAccess', response.data.access)
        await getUserProfile()
      } catch (error) {

      }
    }


    if (!store.state.access && localStorage.getItem('refresh')) {
      restoreAccess()
    }


    setInterval(() => {
      if (store.state.access, store.state.user) {
        restoreAccess()
        getUserProfile()
      }
    }, 59_000)

    const loading = ref(true)

    setTimeout(() => {
      loading.value = false
    }, 2000)

    return {
      loading
    }
  },
}
</script>

<style>
.loader-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loader-inner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>


