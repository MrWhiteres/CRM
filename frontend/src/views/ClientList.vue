<template>
  <v-card class="base-container" outlined shaped>
    <v-card-title>Таблица новых клиентов:
    </v-card-title>
    <v-card-title>{{ currentDate }}</v-card-title>
    <v-container style="min-width: 100%" v-if="showTable">
      <v-form @submit.prevent="submitForm">
        <v-skeleton-loader :loading="loading_skeleton" boilerplate type="article">
          <v-data-table
            :headers="headers"
            :items="items"
            class="elevation-1"
            height="100%"
            style="min-width: 100%; min-height: 100%;"
            width="100%">
            <template v-slot:item.class_type="{ item }">
              <v-select
                v-model="item.props.title.class_type"
                :items="group_type"
                style="min-width: 135px"
                variant="underlined"
              />
            </template>
            <template v-slot:item.crm_status="{ item }">
              <v-select
                v-model="item.props.title.crm_status"
                :items="crm_status"
                style="min-width: 135px"
                variant="underlined"
              />
            </template>
            <template v-slot:item.coach="{ item }">
              <v-select
                v-model="item.props.title.coach"
                :items="coach_list"
                style="min-width: 135px"
                variant="underlined"
              />
            </template>
            <template v-slot:item.data="{ item }">
              {{ formatDate(item.props.title.data) }}
            </template>
          </v-data-table>
        </v-skeleton-loader>
        <v-btn class="text-success text-caption text-capitalize" style="position: relative; left: 46%; margin-top: 10px"
               type="submit" :loading="loading">Отправить
        </v-btn>
      </v-form>
    </v-container>
    <v-container v-else class="text-center" style="min-width: 100%">
      <v-card>
        <v-alert
          type="info"
          text="Новые заявки отсутствуют!"
          variant="tonal"
        />
      </v-card>
    </v-container>
  </v-card>
</template>

<script>
import axios from "axios";
import {VDataTable, VSkeletonLoader} from "vuetify/labs/components";
import moment from "moment";

export default {
  name: "ClientList",
  components: {
    VDataTable, VSkeletonLoader
  },
  data() {
    return {
      items: [],
      currentDate: new Date().toLocaleDateString("ru-RU", {
        day: "numeric",
        month: "long",
        year: "numeric",
      }),
      loading: false,
      showTable: true,
      loading_skeleton: true,
      headers: [
        {title: "Имя", key: "name"},
        {title: "Фамилия", key: "lastname"},
        {title: "Номер телефона", key: "phone_number"},
        {title: "Секция", key: "section"},
        {title: "Возрастная категория", key: "age"},
        {title: "Тип занятий", key: "class_type"},
        {title: "Дни Посещения", key: "visit_day"},
        {title: "Время Посещения", key: "visit_time"},
        {title: "Статус клиента", key: "crm_status"},
        {title: "Тренер", key: "coach"},
        {title: "Дата добавления", key: "data"},
      ],
      group_type: [],
      crm_status: [],
      coach_list: []
    }
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('client-list/')
        this.items = response.data.elements
        if (this.items.length === 0) {
          this.showTable = false
        }
        this.loading_skeleton = false

        this.crm_status = response.data.crm_status
        this.group_type = response.data.group_type
        this.coach_list = response.data.coach
      } catch (_) {
        this.showTable = false
      }
    },
    async submitForm() {
      try {
        this.loading = true
        await axios.post('client-list/', {clients: this.items})
        await this.fetchData()
        this.loading = false
      } catch (_) {

      }
    },
    formatDate(value) {
      return moment(value).locale('ru').format('DD MMMM YYYY р. HH:mm');
    },
  },
  mounted() {
    this.fetchData()
  }
}
</script>

<style scoped>

</style>
