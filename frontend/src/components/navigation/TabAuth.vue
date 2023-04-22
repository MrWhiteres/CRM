<template>
  <v-list-item
    :subtitle="user.type"
    :title="user.full_name"
  />
  <v-divider class="border-opacity-100 mr-1" vertical/>
  <v-tabs v-model="active_tab">
    <v-tab value="5"
           @click="this.$router.push({name: 'profile'})">
      Профиль
    </v-tab>
    <v-tab value="4" @click="this.$router.push({name: 'form'})">Форма</v-tab>
    <v-tab v-if="['Оператор', 'Администратор'].includes(user.type)"
           value="0" @click="this.$router.push({name: 'clients-all-list'})">
      Таблица клиентов
    </v-tab>
    <v-tab v-if="['Тренер', 'Старший тренер'].includes(user.type)"
           value="1" @click="this.$router.push({name: 'couch-new-client'})">
      Таблица новых клиентов
    </v-tab>
    <v-tab v-if="['Тренер', 'Старший тренер'].includes(user.type)"
           value="2" @click="this.$router.push({name: 'couch-table'})">
      Таблица посещений
    </v-tab>
    <v-tab v-if="['Оператор', 'Администратор'].includes(user.type)"
           value="3" @click="this.$router.push({name: 'client-list'})">
      Таблица новых клиентов
    </v-tab>
    <v-tab v-if="['Оператор', 'Администратор'].includes(user.type)"
           value="Админ панель"
           @click="this.$router.push({name: 'profile'})">Админ панель
    </v-tab>
  </v-tabs>
  <v-spacer/>
  <v-divider class="border-opacity-100" vertical/>
  <v-tabs>
    <v-tab class="text-caption" @click="logout">
      Выйти из учетной записи
    </v-tab>
  </v-tabs>

</template>

<script setup>
import {ref, watch} from "vue";

import router from "@/router";
import {useStore} from "vuex";

const store = useStore()
const active_tab = ref(localStorage.getItem('active_tab' || null))
const user = ref(store.state.user)
setInterval(() => {
  if (user.value !== store.state.user) {
    user.value = store.state.user
  }
})
watch(active_tab, async (newValue) => {
  localStorage.setItem('active_tab', newValue)
})
const logout = async () => {
  localStorage.clear();
  store.commit('clearState')
  await router.push({name: 'auth'});
}
</script>

<style scoped>

</style>
