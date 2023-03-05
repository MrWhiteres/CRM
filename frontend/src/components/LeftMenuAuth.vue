<template>
  <v-list-item
      :prepend-avatar="user.image || 'https://cdn.vuetifyjs.com/images/john.png'"
      :subtitle="returnUserRole(user.type)"
      :title="user.full_name"

  ></v-list-item>


  <v-divider></v-divider>

  <v-list density="compact" nav>
    <v-list-item prepend-icon="mdi-view-dashboard" title="Таблица" value="Таблица"/>
    <v-list-item prepend-icon="mdi-forum" title="Что-то" value="Что-то"/>
    <v-list-item prepend-icon="mdi-account" title="Профиль" value="Профиль"
                 @click="this.$router.push({name: 'profile'})"/>
    <v-list-item v-if="user.type === 'admin'" prepend-icon="mdi-account" title="Админ панель"
                 value="Админ панель"
                 @click="this.$router.push({name: 'profile'})"/>
  </v-list>
</template>

<script>

import {useStore} from "vuex";

export default {
  name: "LeftMenuAuth",
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
      store: useStore(),
      returnUserRole
    }
  }
  ,
  data() {
    return {
      user: this.store.state.user,
    }
  },
  mounted() {
    setInterval(()=> {
      if (this.user.image !== this.store.state.user.image) {
        this.user = this.store.state.user
      }
    })
  }


}
</script>

<style scoped>

</style>