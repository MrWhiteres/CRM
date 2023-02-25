import {createStore} from 'vuex'

export default createStore({
    state: {
        access: "",
        refresh: "",
    },
    getters: {},
    mutations: {
        setAccess(state, access) {
            state.access = access
        },
        setRefresh(state, refresh) {
            state.refresh = refresh
        },
    },
    actions: {
        initializeStore() {
            this.state.refresh = localStorage.getItem("refresh") ? localStorage.getItem("refresh") : ''
        }
    },
    modules: {}
})
