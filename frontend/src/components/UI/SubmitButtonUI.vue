<template>
  <v-btn :text="textButton" type="submit">
  </v-btn>
</template>

<script>
export default {
  name: "submit-button-ui",
  props: {
    textButton: {
      String,
    }
  }
}
</script>

<style scoped>

</style>
