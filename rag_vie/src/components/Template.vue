<script setup>
import {
  ref,
  onBeforeMount,
  onMounted,
  onBeforeUpdate,
  onUpdated,
  onBeforeUnmount,
  onUnmounted,
  onErrorCaptured
} from 'vue';

// Estado reactivo
const message = ref('Hello, World!');

// Método para actualizar el mensaje
const updateMessage = () => {
  message.value = 'Updated message!';
};

// Hook del ciclo de vida - antes de montar
onBeforeMount(() => {
  console.log('onBeforeMount: Component is about to be mounted');
});

// Hook del ciclo de vida - montado
onMounted(() => {
  console.log('onMounted: Component has been mounted');
});

// Hook del ciclo de vida - antes de actualizar
onBeforeUpdate(() => {
  console.log('onBeforeUpdate: Component is about to be updated');
});

// Hook del ciclo de vida - actualizado
onUpdated(() => {
  console.log('onUpdated: Component has been updated');
});

// Hook del ciclo de vida - antes de desmontar
onBeforeUnmount(() => {
  console.log('onBeforeUnmount: Component is about to be unmounted');
});

// Hook del ciclo de vida - desmontado
onUnmounted(() => {
  console.log('onUnmounted: Component has been unmounted');
});

// Hook de captura de errores
onErrorCaptured((err, instance, info) => {
  console.log(`onErrorCaptured: Error captured in component ${instance} with info: ${info}`, err);
  // Puedes devolver false para evitar la propagación del error a otros capturadores
  return false;
});
</script>

<template>
  <div>
    <p>{{ message }}</p>
    <button @click="updateMessage">Update Message</button>
  </div>
</template>

<style scoped>
p {
  color: blue;
}

button {
  margin-top: 10px;
  padding: 5px 10px;
}
</style>