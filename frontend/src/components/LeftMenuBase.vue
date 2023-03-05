<template>
  <v-list-item
      :title="`Гость`"
  ></v-list-item>

  <v-divider></v-divider>

  <v-list density="compact" nav>
    <v-list-item prepend-icon="mdi-account-plus" title="Авторизация" value="Авторизация"
                 @click="this.$router.push({name: 'auth'})"/>
  </v-list>
</template>

<script>
export default {
  name: "LeftMenuBase"
}
</script>

<style scoped>

</style>