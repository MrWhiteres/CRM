<template>
  <v-alert
      v-if="error"
      :title="errorTitle"
      dismissible
      type="error"
      variant="tonal"
      @click="error = null"
  >
    {{ error }}
  </v-alert>
  <v-form @submit.prevent="submitForm">
    <v-container class="container" fluid>
      <v-col>
        <input-ui
            v-model="formData.email"
            :counter="true"
            :dense="true"
            :label="'Email'"
            :maxlength="50"
            :minlength="5"
            :outlined="false"
            :placeholder="'your.best.email@example.com'"
            :rules="[rules.requiredField, rules.email, rules.minLengthEmail]"
            :type="'email'"
            clearable
        />
        <input-ui
            v-model="formData.password"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :counter="true"
            :dense="true"
            :label="'Password'"
            :maxlength="50"
            :minlength="8"
            :outlined="false"
            :rules="[rules.requiredField, rules.minLengthPassword, rules.password]"
            :type="showPassword ? 'text' : 'password'"
            :value="formData.password"
            clearable
            @click:append="showPassword = !showPassword"
        />
      </v-col>
    </v-container>
    <div class="input-wrapper">
      <div class="submit-button-wrapper">
        <submit-button-ui :disabled="loading" :loading="loading"
                          v-text="'Submit'"/>
      </div>
    </div>
    <div class="divider-wrapper">
      <hr class="divider"/>
      <span class="divider-text">OR</span>
      <hr class="divider"/>
    </div>
    <div class="google-auth-wrapper">
      <google-auth @login-failed="handleLoginFailed" @login-successful="handleLoginSuccessful"/>
    </div>
  </v-form>
</template>

<script>

import {email, minLength, required} from "@vuelidate/validators";
import {useVuelidate} from "@vuelidate/core";
import axios from "axios";
import {mapMutations, useStore} from "vuex";
import {useRouter} from "vue-router";
import GoogleAuth from "@/components/GoogleAuth.vue";

const emailPattern = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/
const passwordPattern = /^\S*(?=\S{8,})(?=\S*\d)(?=\S*[A-Z])(?=\S*[a-z])(?=\S*[!@#$%^&*? ])\S*$/
const emailValidate = (value) => {
  return emailPattern.test(value)
}
const passwordValidate = (value) => {
  return passwordPattern.test(value)
}

export default {
  name: "LoginView",
  components: {GoogleAuth},
  setup() {
    const store = useStore();
    const router = useRouter();

    setInterval(() => {
      if (store.state.user && router.currentRoute.value.fullPath === '/auth') {
        router.push({name: 'profile'})
      }
    })

    return {
      v$: useVuelidate(),
      MutationCommand: mapMutations(['clearState']),
      store,
      router
    }
  },
  data() {
    return {
      formData: {
        email: '',
        password: '',
      },
      showPassword: false,
      rules: {
        requiredField: value => !!value || 'Required.',
        email: value => {
          return emailPattern.test(value) || 'Invalid e-mail.'
        },
        minLengthEmail: value => {
          return value.length >= 5 || 'Min length email 5 symbols'
        },
        minLengthPassword: value => {
          return value.length >= 8 || 'Min length password 8 symbols'
        },
        password: value => {
          return passwordPattern.test(value) || 'Invalid password'
        }
      },
      loading: false,
      error: null,
      errorTitle: null,
    }
  },
  validations() {
    return {
      formData: {
        email: {
          required: required,
          email,
          emailValidate
        },
        password: {
          required: required,
          minLengthPassword: minLength(8),
          passwordValidate
        }
      }
    }
  },
  mounted() {
    this.v$.$touch()
  },
  methods: {
    async submitForm() {
      await this.clearSuccessError()
      this.loading = true
      if (this.v$.$invalid) {
        this.errorTitle = 'Форма не валидна.'
        this.error = 'Проверьте данные в форме.'
        this.loading = false
        return
      }
      axios.defaults.headers['Authorization'] = ''
      try {
        const response = await axios.post('login/', this.formData)
        await this.handleLoginSuccessful(response.data)
      } catch (error) {
        await this.showCatch(error)
      }
    },
    async clearSuccessError() {
      this.error = this.errorTitle = null
    },
    async handleLoginSuccessful(data) {
      this.$store.commit('setAccess', data.access);
      this.$store.commit('setRefresh', data.refresh);
      localStorage.setItem('refresh', data.refresh);
      this.loading = false
      await this.router.push({name: 'profile'})
    },
    async handleLoginFailed(error) {
      await this.showCatch(error)
    },
    async showCatch(response) {
      this.errorTitle = 'Ошибка авторизации.'
      if (response.code === 'ERR_NETWORK' || response.request.status === 500) {
        this.errorTitle = 'Ошибка сервера'
        this.error = 'Сервер не отвечает, попробуйте повторить действие позже.'
      } else {
        const status = response.request.status
        const error = response.response.data.error ? response.response.data.error : response.response.data.code
        if ([400, 401].includes(status) && ['UserDoesNotExist', "user_not_found"].includes(error)) {
          this.error = 'Пользователь с таким Email не существует.'
        } else if (status === 400 && error === 'UserInactive') {
          this.error = 'Пользователь не активировал аккаунт, проверьте почту.'
        } else if (status === 400 && error === 'InvalidPassword') {
          this.error = 'Неверный пароль.'
        }
      }
      this.loading = false

    },
  },
}
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 100%;
  position: relative;
}

.input-wrapper {
  min-width: 90%;
  margin-bottom: 1.5rem;
}

.submit-button-wrapper {
  z-index: 2;
  text-align: center;
}


.divider-wrapper {
  display: flex;
  align-items: center;
  margin: 0.5rem 0;
}

.divider {
  flex: 1;
  margin: 0 0.25rem;
  min-width: 150px;
}

.divider-text {
  margin: 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6c757d;
  text-transform: uppercase;
}

.google-auth-wrapper {
  z-index: 1;
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.custom-loader {
  animation: loader 1s infinite;
  display: flex;
}

@-moz-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@-webkit-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@-o-keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes loader {
  from {
    transform: rotate(0);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
