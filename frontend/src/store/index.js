import {createStore} from 'vuex'

export default createStore({
  state: {
    access: "",
    refresh: "",
    user: "",
  },
  getters: {},
  mutations: {
    clearState(state) {
      state.access = ""
      state.refresh = ""
      state.user = ""
    },
    setAccess(state, access) {
      state.access = access
    },
    setRefresh(state, refresh) {
      state.refresh = refresh
    },
    setUser(state, user) {
      state.user = user
    },
  },
  actions: {
    initializeStore() {
      this.state.refresh = localStorage.getItem("refresh") ? localStorage.getItem("refresh") : ''
    },
  },
  modules: {}
})
