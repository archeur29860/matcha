<script setup lang="ts">
import Input from '@/components/input.vue';
import { login } from '@/services/api_authenticate';
import { ref, computed } from 'vue';
import Notification from '@/components/notification.vue'
import { useUserStore } from '@/stores/user';
import { socket } from '@/services/socket';
import { useRouter } from 'vue-router';


const router = useRouter();
const userStore = useUserStore();
const password = ref('');
const notificationRef = ref<InstanceType<typeof Notification> | null>(null);

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const isValidEmail = computed(() => emailRegex.test(userStore.email));

const isFormValid = computed(() => {
    return isValidEmail.value && password.value.trim() !== '';
});

async function handleclick() {
    if (!isFormValid.value) return;

    try {
        const result = await login(userStore.email, password.value)
        const result1 = result.data ?? result
        console.log("Réponse login reçue :", !!result1.access_token);
        console.log("Utilisateur reçu :", !!result1.user);
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
        userStore.username = result1.user.username
        userStore.first_name = result1.user.first_name
        userStore.last_name = result1.user.last_name
        
        // Persistance and sicket
        
        localStorage.setItem('token', result1.access_token)
        userStore.jwt = result1.access_token;
        socket.connect();
        // console.log("Réponse API :", result1)

        notificationRef.value?.make_notification(result)
        await router.push('/home')
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
    <div :class="{ 'email-invalid': userStore.email && !isValidEmail }">
        <Input 
            v-model="userStore.email" 
            type="email" 
            placeholder="exemple@domaine.com" 
        />
    </div>

    <Input v-model="password" type="password" placeholder="password" />
    
    <button 
        v-if="!userStore.jwt" 
        @click="handleclick" 
        :disabled="!isFormValid"
        :class="{ 'btn-disabled': !isFormValid }"
    >JOIN
    </button>
    <button v-else @click="userStore.logout">logout</button>
    <Notification
        ref="notificationRef"
        :show="false"
        position="bottom-left"
    />
    <button 
       @click="$router.push('signup')"
    > create account
    </button>
</template>

<style scoped>

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background-color: #ccc;
}
</style>