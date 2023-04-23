<template>
  <v-card class="base-container" outlined shaped style="max-width: 100%">
    <v-card-title>Таблица новых клиентов:
    </v-card-title>
    <v-card-text>
      <n-space justify="space-between">
        <v-btn :loading="loading" class="text-caption" variant="outlined" @click="fetchData">Обновить таблицу</v-btn>
        <v-btn :loading="submit" class="text-caption" variant="outlined" @click="submitForm">Сохранить данные</v-btn>
      </n-space>
    </v-card-text>
    <v-container style="min-width: 90%">
      <v-data-table
        :headers="headers"
        :items="items"
        :loading="loading"
        :rows-per-page-items="[10, 20, 30]"
        class="elevation-1"
        height="100%"
        style="min-width: 100%; min-height: 100%;"
        width="100%"
      >
        <template v-slot:item.status="{ item }">
          <n-select
            v-model:value="item.props.title.status"
            :options="status"
            style="width: 140px"
          />
        </template>
        <template v-slot:item.details="{ item }">
          {{ item.props.title.details.length }}
        </template>
        <template v-slot:expanded-row="{ columns, item }">
          <div class="text-center">
            <v-dialog
              v-model="dialog"
              width="auto"
            >
              <v-card border rounded>
                <v-card-title class="text-center text-h5">Данные посещения:</v-card-title>
                <v-card-text>
                  <v-card :width="height === 220 ? 260 : 500" border style="padding: 10px">
                    <v-card-subtitle class="text-center">
                      Локация тренировки:
                    </v-card-subtitle>
                    <v-row>
                      <v-col v-for="(location, index) in selected_item.location" :key="index"
                             :cols="height === 220 ? 8 : 7">
                        <v-checkbox
                          v-model="new_item.location"
                          :label="location.title"
                          :value="location.value"
                          color="primary"
                        />
                      </v-col>
                    </v-row>
                    <v-divider class="border-opacity-50" style="margin-top: 10px"/>
                    <v-card-subtitle class="text-center">
                      Тип тренировки:
                    </v-card-subtitle>
                    <v-row>
                      <v-col v-for="(class_type, index) in selected_item.class_type" :key="index"
                             :cols="height === 220 ? 8 : 7">
                        <v-checkbox
                          v-model="new_item.class_type"
                          :label="class_type.title"
                          :value="class_type.title"
                          color="primary"
                        />
                      </v-col>
                    </v-row>
                    <v-divider class="border-opacity-50" style="margin-top: 10px"/>
                    <v-card-subtitle class="text-center">
                      Секция:
                    </v-card-subtitle>
                    <v-row>
                      <v-col v-for="(section, index) in selected_item.section" :key="index"
                             :cols="height === 220 ? 6 : 6">
                        <v-checkbox
                          v-model="new_item.section"
                          :label="section.title"
                          :value="section.value"
                          color="primary"
                        />
                      </v-col>
                    </v-row>
                    <v-divider class="border-opacity-50" style="margin-top: 10px"/>
                    <v-card-subtitle class="text-center">
                      Время тренировки:
                    </v-card-subtitle>
                    <v-row>
                      <v-col v-for="(visit_time, index) in selected_item.visit_time" :key="index"
                             :cols="height === 220 ? 5 : 4">
                        <v-checkbox
                          v-model="new_item.visit_time"
                          :label="visit_time.title"
                          :value="visit_time.value"
                          color="primary"
                        />
                      </v-col>
                    </v-row>
                    <v-divider class="border-opacity-50" style="margin-top: 10px"/>
                    <v-card-subtitle class="text-center">
                      Дни тренировки:
                    </v-card-subtitle>
                    <v-row>
                      <v-col v-for="(day, index) in  selected_item.visit_day" :key="index"
                             :cols="height > 220 ? 6 : 12">
                        <v-checkbox
                          v-model="new_item.visit_day"
                          :label="day.title"
                          :value="day.value"
                          color="primary"
                        />
                      </v-col>
                    </v-row>
                    <v-divider class="border-opacity-50" style="margin-top: 10px"/>
                  </v-card>
                </v-card-text>
                <v-card-actions style="display:grid; place-items: center">
                  <v-row>
                    <v-col cols=6>
                      <v-btn class="text-caption" variant="outlined" @click="dialog = false">Отменить</v-btn>
                    </v-col>
                    <v-col cols=6>
                      <v-btn :disabled="button_add" class="text-caption" variant="outlined"
                             @click="new_client(item.props.title)">Добавить
                      </v-btn>
                    </v-col>
                    <v-divider class="border-opacity-100" style="margin-top: 10px"/>
                  </v-row>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </div>
          <tr v-if="item.props.title.status === 'recorded'">
            <td :colspan="columns.length">
              <v-card-subtitle class="text-center">
                <v-btn class="text-caption" variant="outlined"
                       @click="selected_item = item.props.title; dialog = true">Добавить посещение для клиента,
                  {{ item.props.title.fullname }}
                </v-btn>
              </v-card-subtitle>
            </td>
          </tr>
          <tr v-if="item.props.title.details && item.props.title.details.length > 0">
            <td :colspan="columns.length">
              <v-data-table
                :headers="sub_headers"
                :items="item.props.title.details"
                class="elevation-1"
                height="100%"
                style="min-width: 100%; min-height: 100%;"
                width="100%"
              />

            </td>
          </tr>
        </template>
      </v-data-table>
    </v-container>
  </v-card>
</template>
<script setup>
import {computed, ref, watch} from 'vue';
import axios from 'axios';
import {VDataTable} from "vuetify/labs/components";
import {useDisplay} from "vuetify";

const status = ref([
  {'label': 'Записан', 'value': 'recorded'},
  {'label': 'Отказ', 'value': 'not_recorded'},
  {'label': 'Не проверен', 'value': 'not_checked'},
])
const items = ref([]);
const loading = ref(false);
const submit = ref(false);
const dialog = ref(false);
const selected_item = ref(null);
const new_item = ref({
  class_type: '',
  section: '',
  visit_time: '',
  visit_day: '',
  location: ''
})
const expand = ref([]);
const headers = [
  {title: "", key: "data-table-expand"},
  {title: 'Фамилия Имя', key: 'fullname'},
  {title: 'Номер телефона', key: 'phone_number'},
  {title: 'Статус клиента', key: 'status'},
  {title: 'Количество записей', key: 'details'},
];
const subHeaders = ref([
  {title: "Место проведения", key: "location"},
  {title: "День проведения", key: "visit_day"},
  {title: "Время проведения", key: "visit_time"},
  {title: "Секция", key: "section"},
  {title: "Тип группы", key: "class_type"},
])
const button_add = ref(true)
const sub_headers = ref([
  {
    title: "Место проведения",
    key: "location",
  },
  {
    title: "День проведения",
    key: "visit_day",
  },
  {
    title: "Время проведения",
    key: "visit_time",
    width: 150,
  },
  {
    title: "Секция",
    key: "section",
  },
  {
    title: "Тип группы",
    key: "class_type",
  },
])
const {name} = useDisplay()
const height = computed(() => {
  switch (name.value) {
    case 'xs':
      return 220
    case 'sm':
      return 400
    case 'md':
      return 500
    case 'lg':
      return 600
    case 'xl':
      return 800
    case 'xxl':
      return 1200
  }

  return undefined
})
const new_client = async (value) => {
  if (!selected_item.details) {
    selected_item.details = []
  }
  value.details.push(new_item.value)
  new_item.value = {
    class_type: '',
    section: '',
    visit_time: '',
    visit_day: '',
    location: ''
  }
  dialog.value = false
}
watch(new_item, async () => {
  button_add.value = !(
    new_item.value.class_type.length > 0 &&
    new_item.value.section.length > 0 &&
    new_item.value.visit_time.length > 0 &&
    new_item.value.visit_day.length > 0
  )
}, {deep: true})
const fetchData = async () => {
  try {
    loading.value = true;
    const response = await axios.get('new-clients/');
    items.value = response.data.elements
  } catch (_) {
  } finally {
    loading.value = false;
  }
};


const submitForm = async () => {
  try {
    submit.value = true
    await axios.post("new-clients/", {data: items.value});
    await fetchData()
  } catch (_) {
  }
  submit.value = false
}
fetchData();
</script>
<style scoped>

</style>
