<template>
  <v-btn prepend-icon="mdi-google-plus">
    {{ buttonText }}
  </v-btn>
</template>

<script>
export default {
  name: "gb-ui",
  props: ['buttonText']
}
</script>

<style scoped>
</style>
