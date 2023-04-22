<template>
  <v-card class="base-container" outlined shaped>
    <v-card-title>Таблица посещения:</v-card-title>
    <v-card-title>{{ currentDate }}</v-card-title>
    <v-container>
      <v-form @submit.prevent="submitForm">
        <v-data-table
          v-model:items-per-page="itemsPerPage"
          :headers="headers"
          :items="clients"
          class="elevation-1"
          height="100%"
          style="min-width: 100%; min-height: 100%;"
          width="100%">
          <template v-slot:top>
            <v-toolbar flat>
              <v-spacer/>
              <v-btn class="text-caption" @click="fetchData" v-text="`Обновить данные`"/>
              <v-dialog v-model="dialog" max-width="500px" persistent>
                <template v-slot:activator="{ props }">
                  <v-btn
                    color="black"
                    icon
                    v-bind="props"
                  >
                    <v-icon>mdi-account-plus-outline</v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">Анкета посетителя</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12" md="4" sm="6">
                          <v-text-field v-model="editedItem.first_name" label="Имя" variant="underlined"/>
                        </v-col>
                        <v-col cols="12" md="4" sm="6">
                          <v-text-field v-model="editedItem.last_name" label="Фамилия" variant="underlined"/>
                        </v-col>
                        <v-col cols="12" md="4" sm="6">
                          <v-text-field v-model="editedItem.phone_number" label="Номер телефона" variant="underlined"/>
                        </v-col>
                        <v-col cols="12" md="4" sm="6">
                          <v-select v-model="editedItem.visit_time" :items="timeItems" label="Время тренировки"
                                    variant="underlined"/>
                        </v-col>
                        <v-col cols="12" md="4" sm="6">
                          <v-select v-model="editedItem.class_type" :items="class_type" label="Тип тренировки"
                                    variant="underlined"/>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn class="text-caption" color="blue-darken-1" variant="text" @click="close">Закрыть</v-btn>
                    <v-btn
                      :disabled="!Boolean(editedItem.first_name) || !Boolean(editedItem.last_name) || !Boolean(editedItem.phone_number) || !Boolean(editedItem.visit_time) || !Boolean(editedItem.class_type) "
                      class="text-caption"
                      color="blue-darken-1"
                      variant="text" @click="save">Добавить
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:item.exist="{ item }">
            <v-checkbox-btn v-if="Boolean(item.props.title)" v-model="item.props.title.exist" color="success"
                            style="max-width: 10px"
                            variant="underlined"
            />
            <v-checkbox-btn v-else v-model="item.value.exist" color="success" variant="underlined"/>
          </template>
          <template v-slot:item.full_name="{ item }">
            <v-text-field
              :value="`${item.value.last_name ? `${item.value.last_name || ''} ${item.value.first_name}` :` ${item.props.title.first_name}`}`"
              readonly
              variant="underlined"/>

          </template>
          <template v-slot:item.payed="{ item }">
            <v-text-field
              v-if="Boolean(item.props.title)"
              :disabled="!item.props.title.exist"
              v-model="item.props.title.payed"
              style="min-width: 100px"
              type="number"
              variant="underlined"/>
            <v-text-field
              v-else
              :disabled="!item.value.exist"
              v-model="item.value.payed"
              style="min-width: 100px"
              type="number"
              variant="underlined"/>
          </template>
          <template v-slot:item.status="{ item }">
            <v-select
              v-if="Boolean(item.props.title)"
              :disabled="!item.props.title.exist"
              v-model="item.props.title.status"
              :items="payedStatus"
              style="min-width: 100px"
              variant="underlined"/>
            <v-select
              v-else
              v-model="item.value.status"
              :disabled="!item.value.exist"
              :items="payedStatus"
              style="min-width: 204px"
              variant="underlined"/>
          </template>
          <template v-slot:item.info="{ item }">
            <v-text-field
              v-if="Boolean(item.props.title)"
              v-model="item.props.title.info"
              style="min-width: 204px"
              variant="underlined"/>
            <v-text-field
              v-else
              v-model="item.value.info"
              style="min-width: 204px"
              variant="underlined"/>
          </template>
          <template v-slot:item.payed_status="{ item }">
            <v-list>
              <v-list-item
                v-if="Boolean(item.props.title)"
                style="min-width: 100px"
              >
                {{ item.props.title.payed_status }}
              </v-list-item>
              <v-list-item
                v-else
                style="min-width: 100px"
              >
                {{ item.value.payed_status }}
              </v-list-item>
            </v-list>
          </template>
        </v-data-table>
        <v-btn class="btn-submit" color="primary" type="submit">
          Сохранить
        </v-btn>
      </v-form>
    </v-container>
  </v-card>
</template>
<script>
import {VDataTable} from "vuetify/labs/components";
import axios from "axios";

export default {
  name: "CouchTable",
  components: {VDataTable},
  data() {
    return {
      isMobile: false,
      currentDate: new Date().toLocaleDateString("ru-RU", {
        day: "numeric",
        month: "long",
        year: "numeric",
      }),
      dialog: false,
      dialogDelete: false,
      itemsPerPage: 0,
      paidStatus: [],
      payedStatus: [
        {title: 'Полная оплата', value: 'full'},
        {title: 'Частичная оплата', value: 'part'},
        {title: 'Первая тренировка', value: 'first'},
        {title: 'Поразово', value: 'one_paid'},
      ],
      headers: [
        {title: "Фамилия имя", key: "full_name"},
        {title: "Посещение", key: "exist"},
        {title: "Оплата", key: "payed"},
        {title: "Статус оплаты", key: "status"},
        {title: "Текущий статус", key: "payed_status"},
        {title: "Доп информация", key: "info"},
      ],
      clients: [],
      editedIndex: -1,
      editedItem: {
        first_name: "",
        last_name: "",
        phone_number: "",
        visit_time: "",
        class_type: ""
      },
      timeItems: [],
      class_type: []
    };
  },
  methods: {
    async submitForm() {
      try {
        await axios.post('clients-date/', {clients: this.clients})
        await this.fetchData()
      } catch (_) {
      }
    },
    async save() {
      if (this.editedIndex > -1) {
        Object.assign(this.clients[this.editedIndex], this.editedItem);
      } else {
        this.clients.push(this.editedItem);
      }
      this.itemsPerPage = this.clients.length
      await this.close();
    },
    async close() {
      this.dialog = false;
      this.editedItem = {
        exist: false,
        info: "",
      };
      this.editedIndex = -1;
    },
    async fetchData() {
      try {
        this.clients = []
        const response = await axios.get('clients-date/')
        this.clients = response.data.clients
        this.itemsPerPage = this.clients.length
        this.timeItems = response.data.time
        this.paidStatus = response.data.status_paid
        this.class_type = response.data.class_type
      } catch (_) {

      }
    },
  },
  mounted() {
    this.fetchData()
  }
}
</script>

<style scoped>
.base-container {
  left: 10%;
  max-width: 80%;
  min-width: 70%;
}

.btn-submit {
  position: relative;
  margin-top: 10px;
}

@media screen and (max-width: 1260px) {
  .btn-submit {
    left: 75%;
  }
}


@media screen and (max-width: 767px) {
  .base-container {
    left: 0;
    min-width: 100%;
    font-size: 15px;
  }

  .btn-submit {
    position: relative;
    margin-top: 10px;
    left: 64%;
  }
}

</style>
