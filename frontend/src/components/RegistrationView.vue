<template>
    <v-form @submit.prevent="submitForm">
        <v-container class="registrationPage" fluid>
            <v-col class="registrationPage">
                <input-ui
                        v-model="formData.username"
                        :counter="true"
                        :dense="true"
                        :label="'Username'"
                        :maxlength="50"
                        :minlength="5"
                        :outlined="false"
                        :placeholder="'Best Username'"
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
                <submit-button-ui v-text="'Submit'"/>
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
    <modal-base-ui
            v-show="isModalVisible"
            :modal-body="modalBody"
            :modal-head="modalHeader"
            :text-button="textButton"
            @close="modalButton"
    />
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
                username: '',
                email: '',
                password: '',
                confirm_password: '',
            },
            isModalVisible: false,
            modalHeader: '',
            modalBody: '',
            textButton: 'Закрыть',
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
            modalButton: this.closeModal
        }
    },
    validations() {
        return {
            formData: {
                username: {
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
        submitForm() {
            this.v$.$touch()
            if (this.v$.$invalid) {
                this.modalHeader = 'Форма не валидна.'
                this.modalBody = 'Проверьте данные в форме.'
                this.showModal()
                return
            }
            axios
                .post("registration/", this.formData)
                .then(() => {
                    this.showThen()
                })
                .catch(response => {
                    this.showCatch(response)
                })
        },
        showModal() {
            this.isModalVisible = true;
        },
        closeModal() {
            this.isModalVisible = false;
        },
        clearForm() {
            this.formData = {
                username: '',
                email: '',
                password: '',
                confirm_password: '',
            }
        },
        showThen() {
            this.modalHeader = 'Регистрация успешна!'
            this.modalBody = 'Вы успешно зарегистрировались, сейчас вам на почту было отправлено письмо для активации вашего аккаунта на сайте.'
            this.showModal()
            this.clearForm()
        },
        showCatch(response) {
            this.modalHeader = 'Ошибка регистрации.'
            if (response.code === 'ERR_NETWORK' || response.request.status === 500) {
                this.modalHeader = 'Ошибка сервера'
                this.modalBody = 'Сервер не отвечает, попробуйте повторить действие позже.'
            } else {
                const status = response.request.status
                const error = response.response.data.error
                if (status === 400 && error === 'UserExist') {
                    this.modalBody = 'Пользователь с таким Username или Email уже существует.'
                } else if (status === 400 && error === 'InvalidPassword') {
                    this.modalBody = 'Введен некорректный пароль.'
                }
            }

            this.showModal()
        },
        handleRegistrationSuccessful(data) {
            this.showThen()
            console.log("Login successful!", data);

        },
        handleRegistrationFailed(error) {
            this.showCatch(error)
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
</style>