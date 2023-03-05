<template>
  <v-app-bar>
    <v-app-bar-nav-icon @click="drawer = !drawer"/>
  </v-app-bar>
  <v-navigation-drawer
      v-model="drawer"
      temporary
  >
    <left-menu-auth v-if="store.state.user"/>
    <left-menu-base v-else/>
    <template v-if="store.state.user" v-slot:append>
      <div class="pa-2">
        <v-btn block @click="logout">
          Logout
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import {useStore} from "vuex";
import LeftMenuAuth from "./LeftMenuAuth.vue";
import LeftMenuBase from "./LeftMenuBase.vue";
import {useRouter} from "vue-router";

export default {
  name: "NavBar",
  components: {LeftMenuBase, LeftMenuAuth},
  data() {
    return {
      drawer: false,
      group: null,
    }
  },
  setup() {
    const router = useRouter();
    const store = useStore();
    const logout = async () => {
      localStorage.clear();
      store.commit('clearState')
      await router.push({name: 'auth'});
    }

    return {
      store,
      logout
    }

  },
}
</script>

<style scoped>

</style>
