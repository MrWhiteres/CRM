<template>
  <v-responsive>
    <v-sheet :class="`ml-${height > 220 ? 5 : 0} mr-${height > 220 ? 5 : 0} mt-2 mb-5` " style="padding: 10px;">
      <v-card class="v-card-base" elevation="20">
        <v-card-title v-if="height > 220">
          Таблица посещений за: {{ currentDate }}
        </v-card-title>
        <v-card-title v-if="height === 220">
          Таблица посещений за:
        </v-card-title>
        <v-card-title v-if="height === 220">
          {{ currentDate }}
        </v-card-title>
        <v-card-text>
          <n-space justify="space-between">
            <v-btn :loading="button_update" class="text-caption mb-1" variant="outlined" @click="fetchData">
              Обновить таблицу
            </v-btn>
            <v-spacer/>
            <v-btn append-icon="mdi-account-plus-outline" class="text-caption mb-1" variant="outlined"
                   @click="dialog=true">
              Добавить нового ученика:
            </v-btn>
          </n-space>
        </v-card-text>
        <v-dialog v-model="dialog" max-width="600px">
          <v-card border rounded>
            <v-card-title class="text-center text-h5">Анкета нового клиента:</v-card-title>
            <v-card-text>
              <v-sheet border style="padding: 10px">
                <v-text-field v-model="new_item.fullname"
                              :rules="[rules.requiredField, rules.isString, rules.minLength]"
                              label="Фамилия Имя"
                              variant="underlined"/>
                <v-text-field v-model="new_item.phone_number"
                              :rules="[rules.requiredField, rules.isNumber, rules.minLengthNumber]"
                              label="Номер телефона" variant="underlined"/>
                <v-card-subtitle class="text-center">
                  Тип тренировки:
                </v-card-subtitle>
                <v-row>
                  <v-col v-for="(class_type, index) in class_type" :key="index" :cols="height === 220 ? 8 : 6">
                    <v-checkbox
                      v-model="new_item.class_type"
                      :label="class_type.title"
                      :value="class_type.value"
                      color="primary"
                    />
                  </v-col>
                </v-row>
                <v-divider class="border-opacity-50" style="margin-top: 10px"/>
                <v-card-subtitle class="text-center">
                  Возрастная категория:
                </v-card-subtitle>
                <v-row>
                  <v-col v-for="(age, index) in ages" :key="index" :cols="height === 220 ? 6 : 4">
                    <v-checkbox
                      v-model="new_item.age"
                      :label="age.title"
                      :value="age.value"
                      color="primary"
                    />
                  </v-col>
                </v-row>
                <v-divider class="border-opacity-50" style="margin-top: 10px"/>
                <v-card-subtitle class="text-center">
                  Время тренировки:
                </v-card-subtitle>
                <v-row>
                  <v-col v-for="(visit_time, index) in timeItems" :key="index" :cols="height === 220 ? 5 : 3">
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
                  <v-col v-for="(day, index) in days" :key="index" :cols="height > 220 ? 6 : 12">
                    <v-checkbox
                      v-model="new_item.visit_day"
                      :label="day.title"
                      :value="day.value"
                      color="primary"
                    />
                  </v-col>
                </v-row>
                <v-divider class="border-opacity-50" style="margin-top: 10px"/>
              </v-sheet>
            </v-card-text>
            <v-card-actions style="display:grid; place-items: center">
              <v-row>
                <v-col cols=6>
                  <v-btn class="text-caption" variant="outlined" @click="dialog = false">Отменить</v-btn>
                </v-col>
                <v-col cols=6>
                  <v-btn :disabled="button_add" class="text-caption" variant="outlined" @click="new_client">Добавить
                  </v-btn>
                </v-col>
                <v-divider class="border-opacity-100" style="margin-top: 10px"/>
              </v-row>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <n-data-table
          :columns="createColumns()"
          :data="data"
          :pagination="pagination"
          :row-key="rowKey"
          class="table-naive"
          :loading="loading"
          size="small"
          @update:checked-row-keys="handleCheck"
        >
          <template v-slot:empty>
            <n-empty description="Данные посещаемости отсутствуют.">
            </n-empty>
          </template>
        </n-data-table>

        <v-card-text style="display: grid; place-items: center">
          <n-space justify="space-between">
            <v-btn :disabled="data.length === 0" :loading="button_submit" append-icon="mdi-account-plus-outline"
                   class="text-caption mb-1"
                   variant="outlined" @click="submit">
              Сохранить и отправить
            </v-btn>
          </n-space>
        </v-card-text>

      </v-card>
    </v-sheet>
  </v-responsive>
</template>
<script setup>

import {NCheckbox, NInput, NInputNumber, NSelect} from "naive-ui";
import {computed, defineComponent, h, ref, watch} from "vue";
import axios from "axios";
import {useDisplay} from "vuetify";

const button_submit = ref(false)
const button_update = ref(false)
const ShowOrEdit = defineComponent({
  props: {
    value: [String, Number],
    onUpdateValue: [Function, Array]
  },
  setup(props) {
    const isEdit = ref(false)
    const inputRef = ref(null)
    const inputValue = ref(props.value)

    function handleOnClick() {
      isEdit.value = true
      nextTick(() => {
        inputRef.value.focus()
      })
    }

    function handleChange() {
      props.onUpdateValue(inputValue.value)
      isEdit.value = false
    }

    return () =>
      h(
        'div',
        {
          style: 'min-height: 22px',
          onClick: handleOnClick
        },
        isEdit.value
          ? h(NInput, {
            ref: inputRef,
            value: inputValue.value,
            onUpdateValue: (v) => {
              inputValue.value = v
            },
            onChange: handleChange,
            onBlur: handleChange
          })
          : props.value
      )
  }
})
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
const loading = ref(true)
const data = ref([])

const check_name = (value) => {
  return /^[\p{L}\s]+$/u.test(value)
}
const currentDate = ref(new Date().toLocaleDateString("ru-RU", {
  day: "numeric",
  month: "long",
  year: "numeric",
}))
const button_add = ref(true)
const new_item = ref({
  id: null,
  fullname: '',
  phone_number: '',
  visit_time: [],
  visit_day: [],
  age: '',
  class_type: '',
  payed: 0,
  status: 'new_client',
  exist: false,
  info: '',
  payed_status: ''
})
const clear_data = () => {
  new_item.value = {
    id: null,
    fullname: '',
    phone_number: '',
    visit_time: [],
    age: '',
    visit_day: [],
    class_type: '',
    payed: 0,
    status: 'new_client',
    exist: false,
    info: '',
    payed_status: ''
  }
}
const new_client = () => {
  data.value.push(new_item.value)
  clear_data()
  dialog.value = false
}

watch(new_item, async () => {
  button_add.value = !(
    check_name(new_item.value.fullname) &&
    new_item.value.fullname.length >= 3 &&
    Boolean(Number(new_item.value.phone_number)) &&
    new_item.value.phone_number.length >= 10 &&
    Number(new_item.value.class_type) > 0 &&
    new_item.value.visit_time.length > 0 &&
    new_item.value.visit_day.length > 0 &&
    toString(new_item.value.age).length > 0
  )
}, {deep: true})

const rules = ref({
  requiredField: value => {
    return !!value || 'Обязательное поле.'
  },
  minLength: value => {
    return !value || value.length >= 3 || 'Минимальная длинна поля составляет 3 символов.'
  },
  minLengthNumber: value => {
    return !value || value.length >= 10 || 'Минимальная длинна поля составляет 10 символов.'
  },
  isNumber: value => {
    return !value || Boolean(Number(value)) || 'Допустимы только цифры.'
  },
  isString: value => {
    return !value || check_name(value) || 'Введены недопустимые символы.'
  }
})
const status = ref([])
const createColumns = () => [
  {
    title: "Фамилия Имя",
    key: "fullname",
    width: 150,
    render(row, index) {
      return h(ShowOrEdit, {
        value: row.fullname,
        onUpdateValue(v) {
          data.value[index].fullname = v;
        }
      });
    }
  },
  {
    title: "Посещение",
    key: "exist",
    render(row, index) {
      return h(NCheckbox, {
        onUpdateChecked(v) {
          data.value[index].exist = v;
        },
      });
    }
  },
  {
    title: "Оплата",
    key: "payed",
    width: 150,
    render(row, index) {
      return h(NInputNumber, {
        value: row.payed,
        placeholder: "Оплата",
        disabled: !row.exist,
        onUpdateValue(v) {
          data.value[index].payed = v;
        }
      });
    }
  },
  {
    title: "Статус оплаты",
    key: "status",
    width: 170,
    render(row, index) {
      return h(NSelect, {
        value: row.status,
        placeholder: 'Статус',
        options: status.value,
        disabled: !row.exist,
        onUpdateValue(v) {
          data.value[index].status = v;
        }
      });
    },

  },
  {
    title: "Текущий статус",
    key: "payed_status"
  },
  {
    title: "Доп информация",
    key: "info",
    height: 100,
    render(row, index) {
      return h(NInput, {
        value: row.info,
        disabled: !row.exist,
        placeholder: 'Доп информация',
        onUpdateValue(v) {
          data.value[index].info = v;
        }
      });
    },
  }
];
const pagination = ref({
  pageSize: 10
})
const rowKey = (row) => row.id
const checkedRowKeysRef = ref([]);
const handleCheck = (rowKeys) => {
  checkedRowKeysRef.value = rowKeys;
}

const dialog = ref(false)
const timeItems = ref([])
const class_type = ref([])
const days = ref([])
const ages = ref([])

const fetchData = async () => {
  try {
    button_update.value = true
    data.value = []
    const response = await axios.get('clients-date/')
    loading.value = false
    data.value = response.data.clients
    class_type.value = response.data.class_type
    timeItems.value = response.data.time
    status.value = response.data.status_paid
    days.value = response.data.visit_day
    ages.value = response.data.ages
  } catch (error) {

  }
  button_update.value = false
}

fetchData()

const submit = async () => {
  try {
    button_submit.value = true
    await axios.post('clients-date/', {clients: data.value}, {headers: {'Content-Type': 'application/json;charset=utf-8'}})
    await fetchData()
  } catch (_) {

  }
  button_submit.value = false
}
</script>

<style scoped>
.v-card-base {
  margin-bottom: 25px;
  padding: 5px;
}

.table-naive {
  overflow: auto;
  white-space: pre;
}
</style>

