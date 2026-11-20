
<script setup lang="ts">
import { ref } from 'vue'
import { send_message, get_chat } from '@/services/api_chat'

const chatId = ref('')
const userId = ref('')
const message = ref('')

const loading = ref(false)
const result = ref<any>(null)

async function testSendMessage() {
  if (!chatId.value || !userId.value || !message.value.trim()) {
    result.value = 'Tous les champs sont obligatoires.'
    return
  }

  loading.value = true
  result.value = await send_message(
    chatId.value,
    userId.value,
    message.value
  )
  loading.value = false

  message.value = ''
}

async function testGetChat() {
  if (!chatId.value) {
    result.value = 'Le chat_id est obligatoire.'
    return
  }

  loading.value = true
  result.value = await get_chat(chatId.value)
  loading.value = false
}
</script>

<template>
  <main class="test-container">
    <h1>Test API Chat</h1>

    <section>
      <h2>Informations</h2>

      <label>Chat ID</label>
      <input v-model="chatId" placeholder="UUID du chat" />

      <label>User ID</label>
      <input v-model="userId" placeholder="UUID de l'utilisateur" />
    </section>

    <section>
      <h2>Envoyer un message</h2>

      <textarea
        v-model="message"
        placeholder="Écris ton message..."
        rows="4"
      />

      <button @click="testSendMessage" :disabled="loading">
        Envoyer
      </button>
    </section>

    <section>
      <h2>Récupérer les messages</h2>

      <button @click="testGetChat" :disabled="loading">
        Récupérer le chat
      </button>
    </section>

    <section v-if="result !== null">
      <h2>Réponse API</h2>
      <pre>{{ typeof result === 'string' ? result : JSON.stringify(result, null, 2) }}</pre>
    </section>
  </main>
</template>

<style scoped>
.test-container {
  max-width: 700px;
  margin: 40px auto;
  padding: 24px;
}

section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

label {
  font-weight: 600;
}

input,
textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font: inherit;
  box-sizing: border-box;
}

button {
  padding: 12px 18px;
  border: none;
  border-radius: 6px;
  background: #397b63;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
}

pre {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
</style>
