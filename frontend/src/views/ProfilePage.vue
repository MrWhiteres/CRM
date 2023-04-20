<template>
  <v-card class="card-base" elevation="20">
    <v-card-title>Профиль пользователя: {{ user.full_name }}</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12" md="3">
          <v-sheet>
            <v-card class="image-profile" elevation="15">
              <v-img
                :src="user.image || 'https://pipesak.com/wp-content/uploads/2019/09/Mike-Place-Holder-PipeSak-About-Page.jpg'"
                contain height="200" rounded></v-img>
            </v-card>
          </v-sheet>
        </v-col>
        <v-col cols="12" md="9">
          <v-sheet>
            <v-card class="personal-info" elevation="10">
              <v-list>
                <v-list-item>
                  <v-list-item-title v-text="'Электронная почта:'"/>
                  <v-list-item-subtitle v-text="user.email"/>
                  <v-divider class="border-opacity-100"/>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title v-text="'Номер телефона:'"/>
                  <v-list-item-subtitle v-if="user.phone_number" v-text="user.phone_number"/>
                  <v-list-item-subtitle v-else v-text="`Не указан.`"/>
                  <v-divider class="border-opacity-100"/>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Тип аккаунта:</v-list-item-title>
                  <v-list-item-subtitle>{{ user.type }}</v-list-item-subtitle>
                  <v-divider class="border-opacity-100"/>
                </v-list-item>
              </v-list>
            </v-card>

          </v-sheet>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions style="justify-content: center">
      <v-btn variant="outlined" @click="editProfile">Редактировать профиль</v-btn>
    </v-card-actions>
  </v-card>

</template>
<script>
import {useRouter} from "vue-router";
import {useStore} from "vuex";
import axios from "axios";

export default {
  name: 'ProfilePage',
  setup() {
    return {
      router: useRouter(),
      store: useStore(),
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
        const response = await axios.get(`user/profile/`)
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
.card-base {
  min-width: 70%;
  margin-bottom: 30px;
}

.image-profile {
  max-width: 71%;
  margin-left: 20px;
}

.personal-info {
  margin-top: 20px;
  max-width: 40%;
}

@media screen and (max-width: 800px) {
  .personal-info {
    max-width: 100%;
    margin-top: 0;
  }
  .image-profile {
    max-width: 55%;
    margin-left: 23%;
  }

}
</style>
