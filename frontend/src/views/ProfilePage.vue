<template>
  <div class="container">
    <v-card class="card-base">
      <v-row>
        <v-col cols="3">
          <v-img :src="user.image || 'https://cdn.vuetifyjs.com/images/john.png'" contain height="200"
                 rounded></v-img>
        </v-col>
        <v-col cols="9">
          <v-card-title>{{ user.full_name }}</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item>
                <v-list-item-title v-text="'Электронная почта:'"/>
                <v-list-item-subtitle v-text="user.email"/>
              </v-list-item>
              <v-list-item>
                <v-list-item-title v-text="'Номер телефона:'"/>
                <v-list-item-subtitle v-if="user.phone_number" :v-text="user.phone_number"/>
                <v-list-item-subtitle v-else v-text="`Не указан.`"/>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Тип аккаунта:</v-list-item-title>
                <v-list-item-subtitle>{{ returnUserRole(user.type) }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-col>
      </v-row>
      <v-card-actions>
        <v-btn variant="outlined" @click="editProfile">Редактировать профиль</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>
<script>
import {useRouter} from "vue-router";
import {useStore} from "vuex";
import axios from "axios";

export default {
  name: 'ProfilePage',
  setup() {
    const returnUserRole = (type) => {
      const userRole = {
        'admin': 'Администратор',
        'user': 'Пользователь',
        'coach': 'Тренер',
        'head_coach': 'Старший тренер',
        'operator': 'Оператор'
      }
      return userRole[type]
    }
    return {
      router: useRouter(),
      store: useStore(),
      returnUserRole
    }
  },
  data() {
    return {
      user: this.store.state.user,
    }
  },
  methods: {
    async getUserProfile() {
      try {
        const response = await axios.get('/user/profile')
        let image = response.data.image
        if (image) {
          response.data.image = await this.getImage()
        }
        this.store.commit('setUser', response.data)
      } catch (error) {
        localStorage.clear()
        this.store.commit('clearState')
        await this.router.push({name: 'auth'})

      }
    },
    async getImage() {
      try {
        const responseImage = await axios.get('user/image/', {responseType: 'blob'})
        return URL.createObjectURL(new Blob([responseImage.data], {type: 'text/plain;charset=utf-8'}))
      } catch (_) {
        localStorage.clear()
        this.store.commit('clearState')
        await this.router.push({name: 'auth'})
      }
    },
    editProfile() {
      this.router.push({name: 'profile-editor'});
    }
  },
  mounted() {
    if (!this.store.state.user) {
      this.router.push({name: 'auth'});
    }
    this.getUserProfile()
    setInterval(() => {
      if (this.user.image !== this.store.state.user.image) {
        this.user = this.store.state.user
      }
    })
  }
}
</script>

<style>
.container {
  max-width: 80%;
}

.card-base {
  min-width: 100%;
  left: 10%;
}
</style>
