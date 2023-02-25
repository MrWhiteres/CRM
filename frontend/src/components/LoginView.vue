<template>
    <v-form @submit.prevent="submitForm">
        <v-container class="loginPage" fluid>
            <v-col class="loginPage">
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
                <submit-button-ui v-text="'Submit'"/>
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
        <v-btn @click="test">
            Click
        </v-btn>
    </v-form>
    <modal-base-ui
            v-show="isModalVisible"
            :modal-body="modalBody"
            :modal-head="modalHeader"
            :text-button="textButton"
            @close="closeModal"
    />
</template>

<script>
import InputUi from "./UI/InputUI.vue";
import GoogleAuth from "./GoogleAuth.vue";
import {email, minLength, required} from "@vuelidate/validators";
import {useVuelidate} from "@vuelidate/core";
import SubmitButtonUi from "./UI/SubmitButtonUI.vue";
import ModalBaseUi from "./UI/ModaBaselUI.vue";
import axios from "axios";

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
    components: {ModalBaseUi, SubmitButtonUi, GoogleAuth, InputUi},
    setup() {
        return {
            v$: useVuelidate()
        }
    },
    data() {
        return {
            formData: {
                email: '',
                password: '',
            },
            isModalVisible: false,
            modalHeader: '',
            modalBody: '',
            textButton: 'Закрыть',
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
        }
    }
    ,
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
    methods: {
        submitForm() {
            this.v$.$touch()
            if (this.v$.$invalid) {
                console.log(this.v$)
                this.modalHeader = 'Форма не валидна.'
                this.modalBody = 'Проверьте данные в форме.'
                this.showModal()
                return
            }
            axios
                .post('login/', this.formData)
                .then(response => {
                    this.handleLoginSuccessful(response.data)
                })
                .catch(response => {
                    console.log(response)
                })
        },
        showModal() {
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },
        handleLoginSuccessful(data) {
            this.$store.commit('setAccess', data.access);
            this.$store.commit('setRefresh', data.refresh);
            localStorage.setItem('refresh', data.refresh);
        },
        handleLoginFailed(error) {
            this.showCatch(error)
        },
        showCatch(response) {
            this.modalHeader = 'Ошибка авторизации.'
            if (response.code === 'ERR_NETWORK' || response.request.status === 500) {
                this.modalHeader = 'Ошибка сервера'
                this.modalBody = 'Сервер не отвечает, попробуйте повторить действие позже.'
            } else {
                const status = response.request.status
                const error = response.response.data.error
                if (status === 400 && error === 'UserDoesNotExist') {
                    this.modalBody = 'Пользователь с таким Email не существует.'
                } else if (status === 400 && error === 'UserInactive') {
                    this.modalBody = 'Пользователь не активировал аккаунт, проверьте почту.'
                } else if (status === 400 && error === 'InvalidPassword') {
                    this.modalBody = 'Неверный пароль.'
                }
            }

            this.showModal()
        },
        test() {
            axios.get('test/').then().catch()
        }
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

.google-auth-wrapper {
    z-index: 1;
    display: flex;
    justify-content: center;
    margin-top: 1.5rem;
}
</style>