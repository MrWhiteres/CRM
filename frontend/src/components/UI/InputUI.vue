<script setup>

</script>

<template>
  <MDBInput :label="labelValue" :type="typeValue" :value="modelValue" @input="updateInput"/>
</template>

<script>
import {MDBInput} from "mdb-vue-ui-kit";

export default {
  name: "input-ui",
  components: {
    MDBInput,
  },
  props: {
    modelValue: [String, Number],
    labelValue: [String],
    typeValue: [String]
  },
  methods: {
    updateInput(event) {
      this.$emit('update:modelValue', event.target.value);
    }
  }

};
</script>

<style scoped>

</style>