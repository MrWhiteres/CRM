<template>
  <v-card>
    <v-container>
      <v-card>
        <v-alert
            v-if="error"
            dismissible
            type="error"
            @click="error = null"
        >
          {{ error }}
        </v-alert>
        <v-form @submit.prevent="updateProfile">
          <v-card-title class="text-center">Редактор профиля</v-card-title>
          <v-container>
            <v-row>
              <v-col>
                <input-ui v-model="userData.first_name"
                          label="Ім'я"
                          readonly/>
                <input-ui v-model="userData.last_name"
                          label="Прізвище"
                          readonly/>
                <input-ui v-if="userData.phone_number"
                          v-model="userData.phone_number"
                          label="Номер телефону"
                          readonly/>
                <input-ui v-else v-model="noneData"
                          label="Номер телефону"
                          readonly/>
                <v-img v-if="userData.image"
                       :aspect-ratio="1"
                       :src="userData.image"
                       cover
                       width="300"/>
                <input-ui v-else
                          v-model="noneData"
                          label="Фотокартка"
                          readonly></input-ui>
              </v-col>
              <v-col>
                <input-ui id="first_name"
                          v-model="updatedUserData.first_name"
                          :counter="true"
                          :dense="true"
                          :maxlength="50"
                          :outlined="false"
                          :placeholder="'Степан'"
                          :rules="[rules.minLength]"
                          :type="'text'"
                          clearable
                          label="Ім'я"
                          prepend-icon="mdi-rename"
                          @change="validateDataChange"
                          @click:clear="validateDataChange"
                />
                <input-ui id="last_name"
                          v-model="updatedUserData.last_name"
                          :counter="true"
                          :dense="true"
                          :maxlength="50"
                          :outlined="false"
                          :placeholder="'Бандера'"
                          :rules="[rules.minLength]"
                          :type="'text'"
                          clearable
                          label="Прізвище"
                          prepend-icon="mdi-rename-box-outline"
                          @change="validateDataChange"
                          @click:clear="validateDataChange"
                />
                <input-ui id="number"
                          v-model="updatedUserData.phone_number"
                          :counter="true"
                          :dense="true"
                          :maxlength="15"
                          :outlined="false"
                          :placeholder="'380998877666'"
                          :rules="[rules.isNumber,rules.minLengthNumber]"
                          :type="'text'"
                          clearable
                          label="Номер телефону"
                          prepend-icon="mdi-card-account-phone"
                          @change="validateDataChange"
                          @click:clear="validateDataChange"
                />
                <v-file-input id="image"
                              v-model="updatedUserData.image"
                              :rules="[rules.isImage]"
                              :show-size="1000"
                              accept="image/*"
                              label="Фотокартка"
                              outlined
                              prepend-icon="mdi-paperclip"
                              @change="validateImageChange($event)"
                              @click:clear="validateImageChange($event)"
                />
              </v-col>
            </v-row>

            <v-alert
                v-if="infoActiv"
                dense
                type="info"
            >
              Поля форми пусті. Для оновлення свого профілю заповніть пусті поля.
            </v-alert>

            <v-btn block @click="router.push({name: 'profile'})">На сторінку профілю</v-btn>
            <v-btn :disabled="isActiv || isLoading" block color="primary" type="submit">
              <span v-if="!isLoading">Оновити профіль</span>
              <span v-else>
               <v-progress-circular color="#ffffff" indeterminate size="20"/>
            </span>
            </v-btn>

          </v-container>
        </v-form>
      </v-card>
    </v-container>
    <v-row justify="center">
      <v-dialog
          v-model="dialog"
          persistent
          width="auto"
      >
        <v-card>
          <v-card-text>Профиль успешно обновлен.</v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
                color="green-darken-1"
                variant="text"
                @click='router.push({name: "profile"})'
            >
              Назад в профиль
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </v-card>
</template>


<script>
import InputUi from "./UI/InputUI.vue";
import {useStore} from "vuex";
import axios from "axios";
import {useRouter} from "vue-router";
import {maxLength, minLength, numeric} from "@vuelidate/validators";
import {useVuelidate} from "@vuelidate/core";

export default {
  name: "ProfileEditor",
  setup() {
    const store = useStore()
    const getCurrentUserData = async () => {
      try {
        const response = await axios.get(`user/profile/`)
        if (
            !(response.data.email === store.state.user.email &&
                response.data.first_name === store.state.user.first_name &&
                response.data.last_name === store.state.user.last_name &&
                response.data.full_name === store.state.user.full_name &&
                response.data.image === store.state.user.image &&
                response.data.phone_number === store.state.user.phone_number &&
                response.data.type === store.state.user.type)
        ) {
          store.commit('setUser', response.data)
        }
      } catch (error) {

      }
    }
    getCurrentUserData()
    return {
      store,
      router: useRouter(),
      v$: useVuelidate(),
    }
  },
  components: {InputUi},
  mounted() {
    setInterval(async () => {
      this.v$.$touch()
    })

  },
  data() {

    return {
      userData: this.store.state.user,
      updatedUserData: {
        firstName: "",
        lastName: "",
        phone_number: '',
        image: [],
      },
      dialog: false,
      noneData: 'Немає інформації',
      isActiv: true,
      isLoading: false,
      infoActiv: true,
      existFieldData: {},
      error: null,
      rules: {
        minLength: value => {
          return !value || value.length >= 5 || 'Мінімальна довжина поля складає 5 символів.'
        },
        minLengthNumber: value => {
          return !value || value.length >= 10 || 'Мінімальна довжина поля складає 10 символів.'
        },
        isNumber: value => {
          return !value || Boolean(Number(value)) || 'Допустимі тільки цифри.'
        },
        isImage: async value => {
          return !value || !value[0] || await this.isImage(value[0]) || 'Обраний файл має недоступний тип.'
        }
      }
    };
  },
  validations() {
    return {
      updatedUserData: {
        first_name: {
          minLength: minLength(5),
          maxLength: maxLength(50),
        },
        last_name: {
          minLength: minLength(5),
          maxLength: maxLength(50),
        },
        phone_number: {
          minLength: minLength(10),
          maxLength: maxLength(15),
          numeric: numeric
        },
      }
    }
  },
  methods: {
    async updateProfile() {
      this.isLoading = true
      if (this.v$.$invalid) {
        this.isLoading = false
      } else {
        try {
          await axios.post('user/profile/', this.updatedUserData, {headers: {'Content-Type': 'multipart/form-data'}})
          this.dialog = true
          this.isLoading = false
        } catch (error) {

        }
      }
    },
    async getDataUpdate() {
      return Boolean(
          this.updatedUserData.first_name ||
          this.updatedUserData.last_name ||
          this.updatedUserData.phone_number ||
          this.updatedUserData.image.length > 0
      )
    },
    async validateDataChange() {
      if (!await this.v$.$invalid && await this.getDataUpdate()) {
        await this.activButton()
      } else {
        await this.disableButton()
        await this.showError()
      }
    },
    async validateImageChange() {
      const image = this.updatedUserData.image[0]
      const result = await this.isImage(image)
      if (image && !await this.v$.$invalid && await this.isImage(image)) {
        await this.activButton()
      } else {
        await this.disableButton()
        await this.showError(image ? !result : false)
      }
    },
    async showError(result = false) {
      if (await this.v$.$invalid && await this.getDataUpdate() || result) {
        this.error = 'Помилка форми.'
        this.infoActiv = false
      }

    }
    ,
    async activButton() {
      this.isActiv = false
      this.infoActiv = false
      this.error = null
    },
    async disableButton() {
      this.isActiv = true
      this.infoActiv = true
      this.error = null
    },
    async isImage(file) {
      try {
        const reader = new FileReader();
        return await new Promise((resolve, reject) => {
          reader.onload = () => {
            const buffer = new Uint8Array(reader.result);
            const header = Array.from(buffer.slice(0, 4)).map(b => b.toString(16)).join('');
            if (header === '89504e47') {
              resolve(true);
            } else {
              resolve(false);
            }
          };
          reader.onerror = () => {
            reject(false);
          };
          reader.readAsArrayBuffer(file);
        });
      } catch (_) {
        return false;
      }
    }
  }
}
</script>

<style scoped>

</style>