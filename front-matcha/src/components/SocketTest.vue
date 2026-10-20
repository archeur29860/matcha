
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { socket } from "../services/socket";

const status = ref("Disconect");
const error = ref("");

function onConnect() {
  status.value = "Connected";
  error.value = "";
}

function onDisconnect() {
  status.value = "Disconect";
}

function onConnectError(err: Error) {
  status.value = "Connexion error";
  error.value = err.message;
}

onMounted(() => {
  socket.on("connect", onConnect);
  socket.on("disconnect", onDisconnect);
  socket.on("connect_error", onConnectError);

  socket.connect();
});

onUnmounted(() => {
  socket.off("connect", onConnect);
  socket.off("disconnect", onDisconnect);
  socket.off("connect_error", onConnectError);

  socket.disconnect();
});
</script>

<template>
  <section>
    <h2>Test WebSocket Matcha</h2>
    <p>État : {{ status }}</p>
    <p v-if="error">Erreur : {{ error }}</p>
  </section>
</template>
