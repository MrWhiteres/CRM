<template>
    <div class="container">
        <v-card class="mx-auto">
            <v-card-title class="text-center">Авторизация</v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col v-if="showLogin" cols="12">
                            <login-view/>
                        </v-col>
                        <v-col v-else cols="12">
                            <registration-view/>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions class="justify-center">
                <v-btn text @click="showLogin = !showLogin">
                    {{ showLogin ? 'Зарегистрироваться' : 'Войти' }}
                </v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script>

import LoginView from "../components/LoginView.vue";
import RegistrationView from "../components/RegistrationView.vue";

export default {
    name: 'Auth',
    components: {
        RegistrationView,
        LoginView

    },
    data() {
        return {
            showLogin: true,
        };
    },
};
</script>

<style>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 85vh;
}
</style>
