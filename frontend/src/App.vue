<script setup>

import LoginView from "./views/LoginView.vue";
import {decodeCredential, GoogleLogin} from "vue3-google-login";

const callback = (response) => {
  // decodeCredential will retrive the JWT payload from the credential
  const userData = decodeCredential(response.credential)
  console.log("Handle the userData", userData)
}
</script>
<template>
  <login-view/>
  <GoogleLogin :callback="callback" auto-login prompt/>
</template>

<script>

</script>

<style scoped>

</style>
