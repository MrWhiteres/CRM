<template>
  <v-responsive>
    <v-app app>
      <div>
        <div v-if="loading" class="loader-container">
          <div class="loader-inner">
            <v-progress-circular :size="64" :width="7" color="primary" indeterminate></v-progress-circular>
          </div>
        </div>

        <div v-else>
          <v-app-bar app>
            <v-app-bar-nav-icon @click="drawer = !drawer"/>
          </v-app-bar>
          <v-navigation-drawer
            v-model="drawer"
            app
            temporary
          >
            <div v-if="store.state.user">
              <left-menu-auth/>
            </div>
            <div v-else>
              <left-menu-base/>
            </div>
            <div v-if="store.state.user">
              <div class="pa-2">
                <v-btn block @click="logout">
                  Выход
                </v-btn>
              </div>
            </div>
          </v-navigation-drawer>
          <v-main>
            <v-responsive>
              <v-container fluid class="v-container">
                <router-view/>
              </v-container>
            </v-responsive>
          </v-main>
        </div>
      </div>
    </v-app>
  </v-responsive>
</template>

<script>

import {computed, ref, watchEffect} from "vue";
import axios from "axios";
import {useStore} from "vuex";
import {useRouter} from "vue-router";
import {useDisplay} from 'vuetify'
import LeftMenuAuth from "@/components/LeftMenuAuth.vue";
import LeftMenuBase from "@/components/LeftMenuBase.vue";

export default {
  name: 'App',
  components: {LeftMenuBase, LeftMenuAuth},
  setup() {
    const store = useStore();
    const {name} = useDisplay()

    const height = computed(() => {
      switch (name.value) {
        case 'xs':
          return 220
        case 'sm':
          return 400
        case 'md':
          return 500
        case 'lg':
          return 600
        case 'xl':
          return 800
        case 'xxl':
          return 1200
      }

      return undefined
    })
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
          } catch (error) {
            localStorage.clear()
            this.store.commit('clearState')
            await this.router.push({name: 'auth'})
          }
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
        localStorage.clear()
        this.store.commit('clearState')
        await this.router.push({name: 'auth'})
      }
    }


    if (!store.state.access && localStorage.getItem('refresh')) {
      restoreAccess()
    }


    setInterval(() => {
      if (store.state.access && store.state.user) {
        restoreAccess()
        getUserProfile()
      }
    }, 59_000)

    const logout = async () => {
      localStorage.clear();
      store.commit('clearState')
      await router.push({name: 'auth'});
    }
    const loading = ref(true) // set the loading initially to true

    const initLoadingTimeout = () => {
      setTimeout(() => {
        loading.value = false
      }, 2000)
    }

    initLoadingTimeout()
    return {
      loading,
      height,
      logout,
      store,
      router
    }
  },
  data() {
    return {
      drawer: false,
      group: null,
    }
  },
}

</script>

<style>
.v-container {
  display: grid;
  place-items: center;
}



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




