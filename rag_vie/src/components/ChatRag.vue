<script setup>
import axios from "axios";
import {ref} from 'vue';

const inputValue = ref('');
const responseValue = ref('');
const queryValue = ref('');

const sendMessage = () => {
  queryValue.value = inputValue.value
  axios.post('/pregunta', {
    "question": inputValue.value
  })

      .then(response => {
        console.log('Datos obtenidos:', response.data);
        responseValue.value = response.data.message
      })
      .catch(error => {
        console.error('Error al obtener los datos:', error);
      });
}
</script>

<template>
  <section class="container-chat">
    <div class="windows-chat">
      <div>
        lado con la informacion del agente
      </div>
      <div class="windows-response">
        <div class="chat-container">
          <div class="bubble-container-1">
            <section v-if="queryValue" class="bubble-chat-1">{{queryValue}}</section>
          </div>
          <div class="bubble-container-2">
            <section v-if="responseValue" class="bubble-chat-2">{{responseValue}}</section>
          </div>
        </div>
        <div class="input-group">
          <input v-model="inputValue" type="text" @keyup.enter="sendMessage">
          <button @click="sendMessage">Enviar</button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
@import "../assets/chat.css";
</style>
