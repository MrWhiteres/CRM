<script setup>
import {decodeCredential, useTokenClient} from "vue3-google-signin";
import axios from "axios";

let email = ''
const handleOnSuccess = async ({access_token}) => {
  try {
    const {data} = await axios.get(`https://www.googleapis.com/oauth2/v3/userinfo?access_token=${access_token}`);
    const email = data.email;
    console.log(access_token, email)
    await axios.post("google/login/", {email, token: access_token});
    console.log("Login successful");
  } catch (error) {
    console.error("Error during login:", error);
  }
};

const handleOnError = (errorResponse) => {
  console.log("Error: ", errorResponse);
};

const {isReady, login} = useTokenClient({
  onSuccess: handleOnSuccess,
  onError: handleOnError,
  // other options
});

const handleSignInSuccess = (response) => {
  const {credential} = response;
  const decodedCredential = decodeCredential(credential);
  const token = credential;
  const email = decodedCredential.email;

  axios
      .post("google/login/", {email, token})
      .then(() => {
        console.log("Login successful");
      })
      .catch((error) => {
        console.error("Error during login:", error);
      });
};
</script>
<template>

  <button :disabled="!isReady" class="google-button" @click="login">
    <svg viewBox="0 0 366 372" xmlns="http://www.w3.org/2000/svg">
      <path d="M305.6 172.3c0-11.4-.9-22.4-2.6-33H187v62.4h84.8c-3.5 18.8-13.8 34.8-29.3 45.3v37.5h47.3c27.7-25.6 43.5-63.3 43.5-111.2z"
            fill="#4285F4"/>
      <path d="M187 324c39.5 0 72.2-13 96.2-35.2l-47.3-37.5c-13 8.7-29.4 13.7-49 13.7-37.8 0-69.7-25.4-81-59.5H62.7v37.2c24.7 48.8 75.2 81.4 134.3 81.4z"
            fill="#34A853"/>
      <path d="M106.1 194.3c-4.4-13-4.4-26.7 0-39.7V117H62.7c-25.1 48.6-25.1 105.4 0 154h43.4v-37.2z" fill="#FBBC05"/>
      <path d="M187 98.8c20.6 0 39.2 7 53.8 20.8l39.9-39.3C259.5 43.1 224.5 24 187 24 128.1 24 77.5 56.5 62.7 112h43.4c11.4-34.1 43.3-57.2 81-57.2z"
            fill="#EA4335"/>
      <path d="M24 24h318v324H24z" fill="none"/>
    </svg>
    Авторизация через Google
  </button>

</template>

<script>
export default {
  name: "GoogleAuth"
};
</script>

<style scoped>

.google-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  background-color: white;
  border: 1px solid #4285F4;
  color: #4285F4;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.google-button:hover {
  background-color: #4285F4;
  color: white;
}

.google-button svg {
  height: 20px;
  width: 20px;
  margin-right: 10px;
}
</style>