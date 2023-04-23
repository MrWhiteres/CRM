<template>
  <v-card class="base-container" outlined shaped>
    <v-card-title>Таблица новых клиентов:
      <v-btn @click="fetchData">Click</v-btn>
    </v-card-title>
    <v-container>
      <v-form @submit.prevent="submitForm">
        <v-skeleton-loader :loading="loading_skeleton" boilerplate type="article">
          <v-data-table
            v-model:items-per-page="itemsPerPage"
            :headers="headers"
            :items="clients"
            class="elevation-1"
            height="100%"
            style="min-width: 100%; min-height: 100%;"
            width="100%"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-card-title>Список новых клиентов:</v-card-title>
              </v-toolbar>
            </template>
            <template v-slot:item.status="{ item }">
              <v-select
                :items="status"
                v-model="item.props.title.status"
                variant="underlined"
              />
            </template>
            <template v-slot:item.lastname="{ item }">
              <v-text-field
                v-model="item.props.title.lastname"
                variant="underlined"
              />
            </template>
            <template v-slot:item.details="{ item }">
              {{ item.props.title.details.length }}
            </template>

            <template v-slot:expanded-row="{ columns, item }">
              <tr v-if="item.props.title.status === 'recorded'">
                <td :colspan="columns.length">
                  <v-data-table
                    :headers="subHeaders"
                    :items="item.props.title.details"
                    class="elevation-1"
                    height="100%"
                    style="min-width: 100%; min-height: 100%;"
                    width="100%"
                  >
                    <template v-slot:top>
                      <v-toolbar flat>
                        <v-card-title>Данные посещения:</v-card-title>
                        <v-dialog v-model="dialog" persistent>
                          <template v-slot:activator="{ props }">
                            <v-spacer/>
                            <v-btn
                              color="black"
                              v-bind="props"
                              @click="clearData"
                              class="text-caption"
                            >
                              Добавить посещение для клиента, {{ item.raw.name }}
                            </v-btn>
                          </template>
                          <v-card>
                            <v-card-title>Добавление новых данных посещения:</v-card-title>
                            <v-card-text>
                              <v-select
                                :items="item.props.title.location"
                                v-model="this.newData.location"
                                label="Локация"
                                variant="outlined"
                              />
                              <v-select
                                :items="item.props.title.visit_day"
                                v-model="this.newData.visit_day"
                                label="День проведения"
                                variant="outlined"
                              />
                              <v-select
                                :items="item.props.title.visit_time"
                                v-model="this.newData.visit_time"
                                label="Время проведения "
                                variant="outlined"
                              />
                              <v-select
                                :items="item.props.title.section"
                                v-model="this.newData.section"
                                label="Секция"
                                variant="outlined"
                              />
                              <v-select
                                :items="item.props.title.class_type"
                                v-model="this.newData.class_type"
                                label="Тип занятий"
                                variant="outlined"
                              />
                            </v-card-text>
                            <v-card-actions>
                              <v-btn color="primary"
                                     :disabled="!this.newData.location.length > 0 || !this.newData.visit_day.length > 0 || !this.newData.visit_time.length > 0 || !this.newData.section.length > 0 || !this.newData.class_type.length > 0"
                                     @click="addNewData(item.props.title)">
                                Добавить
                              </v-btn>
                              <v-btn color="secondary" @click="this.dialog = false">
                                Отмена
                              </v-btn>
                            </v-card-actions>
                          </v-card>
                        </v-dialog>
                      </v-toolbar>
                    </template>
                    <template v-slot:item.class_type="{ item }">
                      {{ returnClassType(item.props.title.class_type) }}
                    </template>
                  </v-data-table>
                </td>
              </tr>
            </template>
          </v-data-table>
          <v-btn class="btn-submit" color="primary" type="submit">
            Сохранить
          </v-btn>
        </v-skeleton-loader>
      </v-form>
    </v-container>
  </v-card>
</template>
<script>
import {VDataTable, VSkeletonLoader} from "vuetify/labs/components";
import axios from "axios";

export default {
  name: "NewClientCouchTable",

  components: {VSkeletonLoader, VDataTable},
  data() {
    return {
      dialog: false,
      loading_skeleton: true,
      headers: [
        {title: "Имя", key: "name"},
        {title: "Фамилия", key: "lastname"},
        {title: "Номер телефона", key: "phone_number"},
        {title: "Статус клиента", key: "status"},
        {title: "", key: "data-table-expand"},
        {title: "Количество записей", key: "details"},
      ],
      subHeaders: [
        {title: "Место проведения", key: "location"},
        {title: "День проведения", key: "visit_day"},
        {title: "Время проведения", key: "visit_time"},
        {title: "Секция", key: "section"},
        {title: "Тип группы", key: "class_type"},
      ],
      clients: [],
      itemsPerPage: 0,
      newData: {
        location: "",
        visit_day: "",
        visit_time: "",
        class_type: "",
        section: ""
      },
      class_type: [{'title': 'Персональные', 'value': 'single'},
        {'title': 'Групповые', 'value': 'group'}],
      status: [
        {'title': 'Записан', 'value': 'recorded'},
        {'title': 'Отказ', 'value': 'not_recorded'},
        {'title': 'Не проверен', 'value': 'not_checked'},
      ]
    };
  },
  methods: {
    async submitForm() {
      try {
        await axios.post("new-clients/", {data: this.clients});
        await this.fetchData()
      } catch (_) {
      }
    },
    async fetchData() {
      try {
        this.clients = []
        this.loading_skeleton = true;
        const response = await axios.get("new-clients/");
        this.clients = response.data.elements.map((client) => ({
          ...client,
          details: client.details || [],
        }));
        this.itemsPerPage = response.data.elements.length;
        this.loading_skeleton = false;
      } catch (_) {
        this.loading_skeleton = false;
      }
    },
    addNewData(item) {
      item.details.push({
        location: this.newData.location,
        visit_time: this.newData.visit_time,
        visit_day: this.newData.visit_day,
        class_type: this.newData.class_type,
        section: this.newData.section,
      });
      this.clearData()
      this.dialog = false;
    },
    clearData() {
      this.newData = {
        location: "",
        visit_day: "",
        visit_time: "",
        class_type: "",
        section: ""
      };
    },
    returnClassType(element) {
      for (let type of this.class_type) {
        if (type.value === element) {
          return type.title
        }
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
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
<!--<v-dialog-->
<!--  v-model="show_info">-->
<!--<v-data-table-->
<!--  :headers="subHeaders"-->
<!--  :items="item.props.title.details"-->
<!--  class="elevation-1"-->
<!--  height="100%"-->
<!--  style="min-width: 100%; min-height: 100%;"-->
<!--  width="100%"-->
<!--&gt;-->
<!--  <template v-slot:top>-->
<!--    <v-toolbar flat>-->
<!--      <v-card-title>Данные посещения:</v-card-title>-->
<!--      <v-dialog v-model="dialog" persistent>-->
<!--        <template v-slot:activator="{ props }">-->
<!--          <v-btn-->
<!--            color="black"-->
<!--            icon-->
<!--            v-bind="props"-->
<!--            @click="clearData"-->
<!--          >-->
<!--            <v-icon>mdi-account-plus-outline</v-icon>-->
<!--          </v-btn>-->
<!--        </template>-->
<!--        <v-card>-->
<!--          <v-card-title>Добавление новых данных посещения:</v-card-title>-->
<!--          <v-card-text>-->
<!--            <v-select-->
<!--              :items="item.props.title.location"-->
<!--              v-model="this.newData.location"-->
<!--              label="Локация"-->
<!--              variant="outlined"-->
<!--            />-->
<!--            <v-select-->
<!--              :items="item.props.title.visit_day"-->
<!--              v-model="this.newData.visit_day"-->
<!--              label="День проведения"-->
<!--              variant="outlined"-->
<!--            />-->
<!--            <v-select-->
<!--              :items="item.props.title.visit_time"-->
<!--              v-model="this.newData.visit_time"-->
<!--              label="Время проведения "-->
<!--              variant="outlined"-->
<!--            />-->
<!--            <v-select-->
<!--              :items="item.props.title.section"-->
<!--              v-model="this.newData.section"-->
<!--              label="Секция"-->
<!--              variant="outlined"-->
<!--            />-->
<!--            <v-select-->
<!--              :items="item.props.title.class_type"-->
<!--              v-model="this.newData.class_type"-->
<!--              label="Тип занятий"-->
<!--              variant="outlined"-->
<!--            />-->
<!--          </v-card-text>-->
<!--          <v-card-actions>-->
<!--            <v-btn color="primary"-->
<!--                   :disabled="!this.newData.location.length > 0 || !this.newData.visit_day.length > 0 || !this.newData.visit_time.length > 0 || !this.newData.section.length > 0 || !this.newData.class_type.length > 0"-->
<!--                   @click="addNewData(item.props.title)">-->
<!--              Добавить-->
<!--            </v-btn>-->
<!--            <v-btn color="secondary" @click="this.dialog = false">-->
<!--              Отмена-->
<!--            </v-btn>-->
<!--          </v-card-actions>-->
<!--        </v-card>-->
<!--      </v-dialog>-->
<!--    </v-toolbar>-->
<!--  </template>-->
<!--  <template v-slot:item.class_type="{ item }">-->
<!--    {{ returnClassType(item.props.title.class_type) }}-->
<!--  </template>-->
<!--</v-data-table>-->
<!--</v-dialog>-->
