<template>
  <div class="login-form">
    <input-ui
        v-model="email"
        :label-value="'Email'"
        :type-value="'email'"
    />
    <input-ui
        v-model="password"
        :label-value="'Password'"
        :type-value="'password'"
    />
    <google-auth/>
  </div>
</template>

<script>
import InputUi from "../components/UI/InputUI.vue";
import GoogleAuth from "../components/GoogleAuth.vue";


export default {
  name: "LoginView",
  components: {GoogleAuth, InputUi},
  data() {
    return {
      email: '',
      password: ''
    }
  }
}
</script>

<style scoped>

</style>