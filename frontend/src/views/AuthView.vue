<template>
  <v-card class="mx-auto card-header">
    <v-card-title class="text-center">Авторизация</v-card-title>
    <v-card-text>
      <v-container>
        <v-row class="container-body">
          <v-col v-if="showLogin">
            <login-view/>
          </v-col>
          <v-col v-else cols="12">
            <registration-view/>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
    <v-card-actions class="justify-center">
      <v-btn text @click="showLogin = !showLogin">
        {{ showLogin ? 'Зарегистрироваться' : 'Войти' }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>

import LoginView from "../components/LoginView.vue";
import RegistrationView from "../components/RegistrationView.vue";
import {useStore} from "vuex";
import {useRouter} from "vue-router";

export default {
  name: 'Auth',
  setup() {
    return {
      store: useStore(),
      router: useRouter()
    }
  },

  components: {
    RegistrationView,
    LoginView
  },
  data() {
    return {
      showLogin: true,
    };
  },
  mounted() {
    if (this.store.state.user) {
      this.router.push({name: 'profile'});

    }
  }
};
</script>

<style>
.card-header {
  max-width: 40%;
}

@media (max-width: 767px) {
  .card-header {
    max-width: 80%;
  }
}

</style>
