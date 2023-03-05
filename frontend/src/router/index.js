import {createRouter, createWebHistory} from "vue-router";
import ConfirmEmailView from "../views/ConfirmEmailView.vue";
import BasePageView from "../views/BasePageView.vue";
import AuthView from "../views/AuthView.vue";
import ProfilePage from "../views/ProfilePage.vue";
import ProfileEditor from "../components/ProfileEditor.vue";

const routes = [
    {path: '/', component: BasePageView, name: 'base', props: true},
    {path: '/auth', component: AuthView, name: 'auth', props: true},
    {path: '/confirm_email/:token', component: ConfirmEmailView, name: 'confirmEmail', props: true},
    {path: '/profile', component: ProfilePage, name: 'profile', props: true},
    {path: '/profile/edit', component: ProfileEditor, name: 'profile-editor', props: true},
]

export default createRouter({
    history: createWebHistory(),
    routes,
})