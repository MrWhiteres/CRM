<template>
  <MDBBtn
      aria-controls="exampleModal"
      color="primary"
      @click="exampleModal=true"
      v-text="btnText"
  >
  </MDBBtn>
  <MDBModal
      id="exampleModal"
      v-model="exampleModal"
      labelledby="exampleModalLabel"
      tabindex="-1"
  >
    <MDBModalHeader>
      <MDBModalTitle id="exampleModalLabel">{{ modalTitle }}</MDBModalTitle>
    </MDBModalHeader>
    <MDBModalBody>{{ modalBody }}</MDBModalBody>
    <MDBModalFooter >
      <MDBBtn color="secondary" @click="exampleModal = false" v-text="btnClose"/>
      <MDBBtn color="primary" v-text="btnSave"/>
    </MDBModalFooter>
  </MDBModal>
</template>
<script>
import {MDBBtn, MDBModal, MDBModalBody, MDBModalFooter, MDBModalHeader, MDBModalTitle,} from 'mdb-vue-ui-kit';
import {ref} from 'vue';

export default {
  name: "modal-ui",
  components: {
    MDBModal,
    MDBModalHeader,
    MDBModalTitle,
    MDBModalBody,
    MDBModalFooter,
    MDBBtn,
  },
  setup() {
    const exampleModal = ref(false);
    return {
      exampleModal,
    };
  },
  props: ['btnText', 'modalBody', 'btnClose', 'btnSave', 'modalTitle']
};
</script>

<style scoped>

</style>