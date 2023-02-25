<template>
    <v-btn type="submit" :text="textButton">
    </v-btn>
</template>

<script>
export default {
    name: "submit-button-ui",
    props: {
        textButton: {
            String,
        }
    }
}
</script>

<style scoped>

</style>
