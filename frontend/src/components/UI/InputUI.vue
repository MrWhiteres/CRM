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
    modelValue: {
      type: [String, Number],
      required: true,
    },
    labelValue: {
      type: String,
      required: true,
    },
    typeValue: {
      type: String,
      required: true,
    }
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