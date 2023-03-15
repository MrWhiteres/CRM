// Composables
import {createRouter, createWebHistory} from 'vue-router'
import CouchTable from "@/views/CouchTable.vue";
import BasePageView from "@/views/BasePageView.vue";
import AuthView from "@/views/AuthView.vue";
import ConfirmEmailView from "@/views/ConfirmEmailView.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import ProfileEditor from "@/components/ProfileEditor.vue";
import FormNewClient from "@/views/FormNewClient.vue";
import ClientList from "@/views/ClientList.vue";

let routes;
routes = [
  {path: '/', component: BasePageView, name: 'base', props: true},
  {path: '/auth', component: AuthView, name: 'auth', props: true},
  {path: '/form', component: FormNewClient, name: 'form', props: true},
  {path: '/confirm_email/:token', component: ConfirmEmailView, name: 'confirmEmail', props: true},
  {path: '/profile', component: ProfilePage, name: 'profile', props: true},
  {path: '/profile/edit', component: ProfileEditor, name: 'profile-editor', props: true},
  {path: '/couch/table', component: CouchTable, name: 'couch-table', props: true},
  {path: '/clients-list/', component: ClientList, name: 'client-list', props: true},
];

export default createRouter({
  history: createWebHistory(),
  routes,
})