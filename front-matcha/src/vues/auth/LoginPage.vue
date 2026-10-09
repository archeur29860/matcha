<script setup lang="ts">
import Input from '@/components/input.vue';
import { login } from '@/services/api_authenticate';
import { ref } from 'vue';
import Notification from '@/components/notification.vue'
import { useUserStore } from '@/stores/user';


const userStore = useUserStore();
const email = ref('')
const password = ref('')
const notificationRef =
    ref<InstanceType<typeof Notification> | null>(null)

async function handleclick() {
    try{
        const result = await login(userStore.email, password.value)
        const result1 = result.data ?? result
        if (!result1.user || !result1.access_token) {
            console.error('answerd format unknow :', result1)
            notificationRef.value?.make_notification({
                error: 'API response don\'t have token or user'
            })
            return
        }

        // pinia store
        userStore.id = String(result1.user.id)
        userStore.email = result1.user.email
        userStore.jwt = result1.access_token

        
        // Persistance
        localStorage.setItem('token', result1.access_token)
        console.log(email.value, password.value)

        notificationRef.value?.make_notification(result)
    }
    catch (error) {
        console.error('Error :', error)

        notificationRef.value?.make_notification({
            error: error instanceof Error
                ? error.message
                : 'Unknow error'
        })
    }
}


</script>


<template>
    <Input v-model="userStore.email" type="email" placeholder="exemple@domaine.com" />
    <Input v-model="password" type="password" placeholder="password" />
    <button v-if="!userStore.jwt" @click="handleclick">SUBMIT</button>
    <button v-else @click="userStore.logout">logout</button>
    <Notification
        ref="notificationRef"
        :show="false"
        position="bottom-left"
    />
</template>