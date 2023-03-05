<template>
    <v-app-bar>
        <v-app-bar-nav-icon @click="drawer = !drawer"/>
    </v-app-bar>
    <v-navigation-drawer
            v-model="drawer"
            temporary
    >
        <v-list-item
                prepend-avatar="https://randomuser.me/api/portraits/men/78.jpg"
                title="John Leider"
        ></v-list-item>

        <v-divider></v-divider>

        <v-list density="compact" nav>
            <v-list-item prepend-icon="mdi-view-dashboard" title="Home" value="home"></v-list-item>
            <v-list-item prepend-icon="mdi-forum" title="About" value="about"></v-list-item>
        </v-list>

        <template v-slot:append>
            <div class="pa-2">
                <v-btn block>
                    Logout
                </v-btn>
            </div>
        </template>
    </v-navigation-drawer>


</template>

<script>
export default {
    name: "NavBar",
    data() {
        return {
            drawer: false,
            group: null,
        }
    }
}
</script>

<style scoped>

</style>