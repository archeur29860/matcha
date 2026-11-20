<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import FormUser from '@/components/formUser.vue'

const formRef = ref<InstanceType<typeof FormUser> | null>(null)
const router = useRouter()
</script>
<template>
    <FormUser/>
    <div class="form-actions">
        <button type="submit" form="user-form">Register</button>
        <button type="button" class="link" @click="router.push('/login')">
        Already have an account?
        </button>
    </div>
</template>