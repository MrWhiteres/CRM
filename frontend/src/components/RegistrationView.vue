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
  <v-alert
      v-if="success"
      :title="successTitle"
      dismissible
      type="success"
      variant="tonal"
      @click="success = null"
  ></v-alert>
  <v-form @submit.prevent="submitForm">
    <v-container class="registrationPage" fluid>
      <v-col class="registrationPage">
        <input-ui
            v-model="formData.first_name"
            :counter="true"
            :dense="true"
            :label="'First Name'"
            :maxlength="50"
            :minlength="5"
            :outlined="false"
            :placeholder="'Stepan'"
            :rules="[rules.requiredField, rules.minLengthUsername]"
            :type="'text'"
            clearable
        />
        <input-ui
            v-model="formData.last_name"
            :counter="true"
            :dense="true"
            :label="'Last name'"
            :maxlength="50"
            :minlength="5"
            :outlined="false"
            :placeholder="'Bandera'"
            :rules="[rules.requiredField, rules.minLengthUsername]"
            :type="'text'"
            clearable
        />
        <input-ui
            v-model="formData.email"
            :counter="true"
            :dense="true"
            :label="'Email'"
            :maxlength="50"
            :minlength="5"
            :outlined="false"
            :placeholder="'your.best.email@example.com'"
            :rules="[rules.requiredField, rules.minLengthEmail, rules.email]"
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
            :rules="[rules.requiredField, rules.password, rules.minLengthPassword]"
            :type="showPassword ? 'text' : 'password'"
            :value="formData.password"
            clearable
            @click:append="showPassword = !showPassword"
        />
        <input-ui
            v-model="formData.confirm_password"
            :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
            :counter="true"
            :dense="true"
            :label="'Confirm Password'"
            :maxlength="50"
            :minlength="8"
            :outlined="false"
            :rules="[rules.requiredField, rules.password, rules.minLengthPassword,rules.passwordConfirmEqual]"
            :type="showConfirmPassword ? 'text' : 'password'"
            :value="formData.confirm_password"
            clearable
            @click:append="showConfirmPassword = !showConfirmPassword"
        />
      </v-col>
    </v-container>
    <div class="input-wrapper">

    </div>

    <div class="input-wrapper">
      <div class="submit-button-wrapper">
        <submit-button-ui :disabled="loading" :loading="loading" v-text="'Submit'"/>
      </div>
    </div>
    <div class="divider-wrapper">
      <hr class="divider"/>
      <span class="divider-text">OR</span>
      <hr class="divider"/>
    </div>
    <div class="google-reg-wrapper">
      <google-registration @registration-failed="handleRegistrationFailed"
                           @registration-successful="handleRegistrationSuccessful"/>
    </div>
  </v-form>
</template>

<script>
import InputUi from "./UI/InputUI.vue";
import GoogleRegistration from "./GoogleRegistration.vue";
import SubmitButtonUi from "./UI/SubmitButtonUI.vue";
import {email, minLength, required, sameAs} from "@vuelidate/validators";
import {useVuelidate} from "@vuelidate/core";
import ModalBaseUi from "./UI/ModaBaselUI.vue";
import axios from "axios";
import {useRouter} from "vue-router";

const emailPattern = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/
const passwordPattern = /^\S*(?=\S{8,})(?=\S*\d)(?=\S*[A-Z])(?=\S*[a-z])(?=\S*[!@#$%^&*? ])\S*$/
const emailValidate = (value) => {
  return emailPattern.test(value)
}
const passwordValidate = (value) => {
  return passwordPattern.test(value)
}

export default {
  name: "RegistrationView",
  components: {ModalBaseUi, SubmitButtonUi, GoogleRegistration, InputUi},
  setup() {
    const v$ = useVuelidate()
    const router$ = useRouter()

    return {
      v$,
      router$,
    }
  },
  data() {
    return {
      formData: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
      },
      error: null,
      errorTitle: null,
      success: null,
      successTitle: null,
      showPassword: false,
      showConfirmPassword: false,
      rules: {
        requiredField: value => !!value || 'Required.',
        email: value => {
          return emailPattern.test(value) || 'Invalid e-mail.'
        },
        minLengthUsername: value => {
          return value.length >= 5 || 'Too short.'
        },
        minLengthEmail: value => {
          return value.length >= 5 || 'Min length email 5 symbols'
        },
        minLengthPassword: value => {
          return value.length >= 8 || 'Min length password 8 symbols'
        },
        password: value => {
          return passwordPattern.test(value) || 'Invalid password'
        },
        passwordConfirmEqual: value => {
          if (this.formData.password) {
            return this.formData.password === value || 'Invalid confirm password'
          }
        }
      },
      loading: false
    }
  },
  validations() {
    return {
      formData: {
        first_name: {
          required: required,
          minLength: minLength(5)
        },
        last_name: {
          required: required,
          minLength: minLength(5)
        },
        email: {
          required: required,
          email: email,
          minLength: minLength(5),
          emailValidate
        },
        password: {
          required: required,
          minLength: minLength(8),
          passwordValidate
        },
        confirm_password: {
          required: required,
          minLength: minLength(8),
          passwordValidate,
          sameAs: sameAs(this.formData.password)
        }
      }
    }
  }
  ,
  methods: {
    async submitForm() {
      this.loading = true
      await this.clearSuccessError()
      this.v$.$touch()
      if (this.v$.$invalid) {
        this.errorTitle = 'Форма не валидна.'
        this.error = 'Проверьте данные в форме.'
        this.loading = false
        return
      }
      try {
        await axios.post("registration/", this.formData)
        await this.showThen()
      } catch (error) {
        await this.showCatch(error)
      }

    },
    async clearForm() {
      this.formData = {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: '',
      }
    },
    async showThen() {
      await this.clearSuccessError()
      this.successTitle = 'Регистрация успешна!'
      this.success = 'Вы успешно зарегистрировались, сейчас вам на почту было отправлено письмо для активации вашего аккаунта на сайте.'
      await this.clearForm()
      this.loading = false
    },
    async clearSuccessError() {
      this.error = this.errorTitle = null
      this.successTitle = this.success = null
    },
    async showCatch(response) {
      await this.clearSuccessError()
      this.errorTitle = 'Ошибка регистрации.'
      if (response.code === 'ERR_NETWORK' || response.request.status === 500) {
        this.errorTitle = 'Ошибка сервера'
        this.error = 'Сервер не отвечает, попробуйте повторить действие позже.'
      } else {
        const status = response.request.status
        const error = response.response.data.error
        if (status === 400 && error === 'UserExist') {
          this.error = 'Пользователь с таким Username или Email уже существует.'
        } else if (status === 400 && error === 'InvalidPassword') {
          this.error = 'Введен некорректный пароль.'
        }
      }
      this.loading = false
    },
    async handleRegistrationSuccessful() {
      await this.showThen()
    },
    async handleRegistrationFailed(error) {
      await this.showCatch(error)
    },


  }
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

.google-reg-wrapper {
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