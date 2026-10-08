<script setup lang="ts">
import Input from '@/components/input.vue';
import { login } from '@/services/api_authenticate';
import { ref } from 'vue';

const email = ref('')
const password = ref('')

async function handleclick() {
    console.log(email.value, password.value)
    const result = await login(email.value, password.value)
}

</script>


<template>
    <Input v-model="email" type="email" placeholder="email" />
    <Input v-model="password" type="password" placeholder="password" />
    <button @click="handleclick">SUBMIT</button>
</template>