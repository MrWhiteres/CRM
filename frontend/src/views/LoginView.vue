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
  </div>
</template>

<script>
import InputUi from "../components/UI/InputUI.vue";

export default {
  name: "LoginView",
  components: {InputUi},
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