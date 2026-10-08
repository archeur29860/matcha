<script setup lang="ts">
import Input from '@/components/input.vue';
import { login } from '@/services/api_authenticate';
import { ref } from 'vue';
import Notification from '@/components/notification.vue'

const email = ref('')
const password = ref('')
const notificationRef =
    ref<InstanceType<typeof Notification> | null>(null)

async function handleclick() {
    console.log(email.value, password.value)
    const result = await login(email.value, password.value)
    notificationRef.value?.make_notification(result)
}

</script>


<template>
    <Input v-model="email" type="email" placeholder="email" />
    <Input v-model="password" type="password" placeholder="password" />
    <button @click="handleclick">SUBMIT</button>
    <Notification
        ref="notificationRef"
        :show="false"
        position="bottom-left"
    />
</template>