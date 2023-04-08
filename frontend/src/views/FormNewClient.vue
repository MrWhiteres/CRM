<template>
  <v-card class="form-client">
    <v-form @submit.prevent="submitForm">
      <v-container>
        <v-card>
          <v-card-title className="text-center">
            Записаться на тренировки
          </v-card-title>
          <v-card-subtitle class="text-caption form-description">
            Для того чтобы начать тренироваться, заполните данную анкету. Свяжитесь с администратором после заполнения.
            Контактный номер:
            +380971916680, +380996374872, +380994687607
          </v-card-subtitle>
        </v-card>
      </v-container>


      <v-container>
        <v-card>
          <v-card-text style="margin-top: 10px">
            <v-select
              v-model="formClient.choice"
              :items="choiceSection"
              label="Тип тренировок:"
              variant="underlined"
              @change="console.log('change event')"
            />
          </v-card-text>
        </v-card>
      </v-container>


      <v-container v-if="['yoga', 'martialArts'].includes(formClient.choice)">
        <v-card>
          <v-card-title class="text-center text-caption">Персональная информация:</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="formClient.name"
              :counter="true"
              :maxlength="50"
              :minlength="3"
              clearable
              label="Имя"
              variant="underlined"
            />
            <v-text-field
              v-model="formClient.phone_number"
              :counter="true"
              :maxlength="50"
              :minlength="3"
              clearable
              label="Номер телефона"
              placeholder="+380778899555"
              variant="underlined"
            />
          </v-card-text>
        </v-card>
      </v-container>


      <v-container v-if="formClient.choice === 'yoga'">
        <v-card>
          <v-card-text>
            <v-select
              v-model="formClient.yoga_type"
              :items="yogaType"
              label="Виды йоги:"
              multiple
              variant="underlined"
            />
            <v-text-field
              v-model="formClient.other_yoga_type"
              :counter="true"
              :maxlength="50"
              :minlength="3"
              label="Другие виды:"
              variant="underlined"
            />
          </v-card-text>
        </v-card>
      </v-container>

      <v-container v-if="formClient.choice === 'martialArts'">
        <v-card>
          <v-card-text>
            <v-select
              v-model="formClient.matrial_arts_type"
              :items="matrialArtsType"
              label="Вид единоборств:"
              multiple
              variant="underlined"
            />
            <v-text-field
              v-model="formClient.other_matrial_arts_type"
              :counter="true"
              :maxlength="50"
              :minlength="3"
              label="Другие виды:"
              variant="underlined"
            />
          </v-card-text>
        </v-card>
      </v-container>


      <v-container v-if="['yoga', 'martialArts'].includes(formClient.choice)">
        <v-card>
          <v-card-title class="text-center text-caption">Общая информация о занятиях:</v-card-title>
          <v-card-text>
            <v-select
              v-model="formClient.class_type"
              :items="classType"
              label="Тип занятий"
              variant="underlined"
            />
            <v-select
              v-model="formClient.training_location"
              :items="states"
              clearable
              label="Локация тренировок (возможно несколько вариантов)"
              multiple
              variant="underlined"
            />

            <v-text-field
              v-model="formClient.other_location"
              :counter="true"
              :maxlength="50"
              :minlength="3"
              clearable
              label="Другие локации:"
              placeholder="Дружбы народов, и тд..."
              variant="underlined"
            />

            <v-select
              v-model="formClient.age"
              :items="fightAge"
              clearable
              label="Возрастная категория:"
              variant="underlined"
            />

            <v-select
              v-model="formClient.training_time"
              :items="trainingTime"
              clearable
              label="Время тренировок:"
              multiple
              variant="underlined"
            />

            <v-select
              v-model="formClient.visit_day"
              :items="visitDay"
              clearable
              label="Дни тренировок (возможно несколько вариантов):"
              multiple
              variant="underlined"
            />
          </v-card-text>

        </v-card>
      </v-container>
      <v-card v-if="['yoga', 'martialArts'].includes(formClient.choice)" class="text-center">
        <v-container>
          <v-btn :disabled="disabled" :loading="loading" class="text-success text-caption text-capitalize"
                 type="submit">Отправить форму
          </v-btn>
        </v-container>

      </v-card>

    </v-form>
    <div class="text-center">
      <v-dialog
        v-model="dialog"
        width="auto"
      >

        <v-card>
          <v-card-text>
            Форма успешно отправлена
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" block @click="dialog = false">Закрыть</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-card>
</template>

<script>

import axios from "axios";

export default {
  name: "FormNewClient",
  data() {
    return {
      loading: false,
      formClient: {
        choice: false,
        name: '',
        phone_number: '',
        class_type: 'group',
        training_location: [],
        other_location: '',
        training_time: [],
        visit_day: [],
        yoga_type: [],
        age: '',
        other_yoga_type: '',
        matrial_arts_type: [],
        other_matrial_arts_type: '',
      },
      clearForm: {
        choice: false,
        name: '',
        phone_number: '',
        class_type: 'group',
        training_location: [],
        other_location: '',
        training_time: [],
        visit_day: [],
        yoga_type: [],
        age: '',
        other_yoga_type: '',
        matrial_arts_type: [],
        other_matrial_arts_type: '',
      },
      dialog: false,
      choiceSection: [
        {title: 'Не выбрано', value: false},
        {title: 'Йога', value: 'yoga'},
        {title: 'Единоборства', value: 'martialArts'},
      ],
      classType: [
        {title: 'Персональные', value: 'single'},
        {title: 'Групповые', value: 'group'},
      ],
      states: [
        {title: 'Позняки (Харьковская, Осокорки, Дарницкий район)', key: 'location_1'},
        {title: 'Лесная', key: 'location_2'},
        {title: 'Троещина', key: 'location_3'},
        {title: 'Героев Днепра', key: 'location_4'},
        {title: 'Оболонь', key: 'location_5'},
        {title: 'Голосеевская', key: 'location_6'},
        {title: 'Теремки / Ипподром / ВДНГ', key: 'location_7'},
        {title: 'Шулявка / Нивки / Берестейка', key: 'location_8'},
        {title: 'Отрадный / Соломенский', key: 'location_9'},
        {title: 'Вокзальная / Университет / Льва Толстого', key: 'location_10'},
        {title: 'Куреневка / Сырец', key: 'location_11'},
        {title: 'Новобеличи', key: 'location_12'},
        {title: 'Кловская / Арсенальная', key: 'location_13'}
      ],
      yogaAge: [
        '6-11', '12-15', '16-25', '25-36', '37-50', '51+'
      ],
      fightAge: [
        '6-11', '12-15', '16-25', '25-36', '37-50', '51+',
      ],
      trainingTime: [
        '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00',
      ],
      visitDay: [
        {title: "Понедельник", key: 'day_1'},
        {title: "Вторник", key: 'day_2'},
        {title: "Среда", key: 'day_3'},
        {title: "Четверг", key: 'day_4'},
        {title: "Пятница", key: 'day_5'},
        {title: "Суббота", key: 'day_6'},
        {title: "Воскресенье", key: 'day_7'},
        {title: "Плавающий график, постоянно разные дни", key: 'day_8'},
        {title: "Не принципиально, могу и буду ходить в любые дни", key: 'day_9'},
      ],
      yogaType: [
        {title: "Хатха-йога", key: 'yoga_sec_1'},
        {title: "Хот-йога", key: 'yoga_sec_2'},
        {title: "Флай-йога", key: 'yoga_sec_3'},
        {title: "Йога для беременных", key: 'yoga_sec_4'},
        {title: "Йога после родов", key: 'yoga_sec_5'},
      ],
      matrialArtsType: [
        {title: "Бокс", key: 'mat_sec_1'},
        {title: "Кикбоксинг/Тайский бокс", key: 'mat_sec_2'},
        {title: "ММА / Панкратион", key: 'mat_sec_3'},
        {title: "Рукопашный бой / Самооборона", key: 'mat_sec_4'},
        {title: "Айкидо", key: 'mat_sec_5'},
        {title: "Карате", key: 'mat_sec_6'},
        {title: "Тхеквондо", key: 'mat_sec_7'},
        {title: "Джиуджитсу / Грепплинг", key: 'mat_sec_8'},
        {title: "Борьба (Вольная/Самбо)", key: 'mat_sec_9'},
        {title: "Дзюдо / Самбо", key: 'mat_sec_10'}
      ],
      disabled: true
    }
  },
  methods: {
    async submitForm() {
      this.loading = true
      try {
        await axios.post('forms/', {data: this.formClient})
        this.loading = false
        this.formClient = this.clearForm
        this.dialog = true
      } catch (_) {
        this.loading = false
      }
    },
    async activateButton() {

      if (this.formClient.choice === 'yoga') {
        this.disabled = await this.checkAnswer(await this.checkYogaField())
      }
      if (this.formClient.choice === 'martialArts') {
        this.disabled = await this.checkAnswer(await this.checkMartialArtsField())
      }
    },
    async checkYogaField() {
      return [
        this.formClient.name.length > 3,
        this.formClient.phone_number.length > 10,
        this.formClient.training_location.length > 0 || this.formClient.other_location.length > 3,
        this.formClient.training_time.length > 0,
        this.formClient.visit_day.length > 0,
        this.formClient.yoga_type.length > 0 || this.formClient.other_yoga_type.length > 3,
      ]
    },
    async checkMartialArtsField() {
      return [
        this.formClient.name.length > 3,
        this.formClient.phone_number.length > 10,
        this.formClient.training_location.length > 0 || this.formClient.other_location.length > 3,
        this.formClient.training_time.length > 0,
        this.formClient.visit_day.length > 0,
        this.formClient.matrial_arts_type.length > 0 || this.formClient.other_matrial_arts_type.length > 3,
      ]
    },
    async checkAnswer(data) {
      for (let element of data) {
        if (!element) {
          return true
        }
      }

      return false
    },
    clearDataForm() {
      this.formClient.other_matrial_arts_type = ''
      this.formClient.matrial_arts_type = []
      this.formClient.yoga_type = []
      this.formClient.other_yoga_type = ''
    }
  },
  mounted() {
    try {
      setInterval(() => {
        this.activateButton()
      })
    } catch (_) {
    }

  },
  watch: {
    'formClient.choice': function () {
      this.clearDataForm()
    }
  }
}

</script>

<style scoped>
.form-description {
  font-size: 14px;
  line-height: 20px;
  text-align: center;
  white-space: normal;
}

.form-client {
  max-width: 60%;
  left: 18%;
}

@media screen and (max-width: 768px) {
  .form-description {
    font-size: 16px;
    line-height: 24px;
  }

  .form-client {
    max-width: 100%;
    min-width: 100%;
    left: 0;
  }
}


</style>
