<template>
  <v-list-item
    :subtitle="returnUserRole(user.type)"
    :title="user.full_name"

  ></v-list-item>

  <v-divider></v-divider>

  <v-list density="compact" nav>

    <v-list-item v-if="['operator', 'admin'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard-outline " title="Таблица клиентов"
                 value="Таблица клиентов" @click="this.$router.push({name: 'clients-all-list'})"/>

    <v-list-item v-if="['coach', 'head_coach'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard" title="Таблица новых клиентов"
                 value="Таблица новых клиентов" @click="this.$router.push({name: 'couch-new-client'})"/>


    <v-list-item v-if="['coach', 'head_coach'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard" title="Таблица посещений"
                 value="Таблица" @click="this.$router.push({name: 'couch-table'})"/>

    <v-list-item v-if="['operator', 'admin'].includes(user.type)"
                 prepend-icon="mdi-view-dashboard" title="Таблица новых клиентов"
                 value="Таблица новых клиентов" @click="this.$router.push({name: 'client-list'})"/>

    <v-list-item prepend-icon="mdi-form-select" title="Форма" value="Форма" @click="this.$router.push({name: 'form'})"/>

    <v-list-item prepend-icon="mdi-account-circle" title="Профиль" value="Профиль"
                 @click="this.$router.push({name: 'profile'})"/>

    <v-list-item v-if="user.type === 'admin'" prepend-icon="mdi-account-circle-outline" title="Админ панель"
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
    setInterval(() => {
      if (this.user.image !== this.store.state.user.image) {
        this.user = this.store.state.user
      }
    })
  }


}
</script>

<style scoped>

</style>
