import {createRouter, createWebHistory} from "vue-router";
import ConfirmEmailView from "../views/ConfirmEmailView.vue";
import BasePageView from "../views/BasePageView.vue";
import AuthView from "../views/AuthView.vue";

const routes = [
    {path: '/', component: BasePageView, name: 'base'},
    {path: '/auth', component: AuthView, name: 'login', props: true},
    {path: '/confirm_email/:token', component: ConfirmEmailView, name: 'confirmEmail'},
]

export default createRouter({
    history: createWebHistory(),
    routes,
})