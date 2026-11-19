<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useForm, Field as VeeField } from 'vee-validate'

import Input from '@/components/input.vue'
import { signupSchema } from '@/validation/signupSchema'
import { useUserStore } from '@/stores/user'
import { login } from '@/services/api_authenticate'
import { socket } from '@/services/socket'
import Notification from '@/components/notification.vue'

const notificationRef = ref<InstanceType<typeof Notification> | null>(null)

const router = useRouter();
const userStore = useUserStore()
const formError = ref('')

const { handleSubmit, isSubmitting } = useForm({
  validationSchema: signupSchema,
  initialValues: {
    email: '',
    password: '',
    pwd: '',
    username: '',
    first_name: '',
    last_name: '',
  },
})
// const { handleSubmit, values, isSubmitting } = useForm({
//   initialValues: {
//     email: '', password: '', pwd: '', username: '',
//     first_name: '', last_name: '',
//   },
// })


const onSubmit = handleSubmit(async (form) => {
    formError.value = ''
    try {
        const response = await fetch(
            'http://localhost:5000/api/users/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: form.email.trim(),
                    username: form.username.trim(),
                    first_name: form.first_name.trim(),
                    last_name: form.last_name.trim(),
                    password: form.password,
                }),
            }
        );

        const data = await response.json();

        notificationRef.value?.make_notification({ ...data, status: response.status })
        if (!response.ok) return

        console.log('Utilisateur créé :', data);

        // Redirection vers la connexion
        if (!result.access_token || !result.user) {
        notificationRef.value?.make_notification({
            error: { code: 'LOGIN_FAILED', 
            message: "Creation, but it's impossible to connect" },
            status: 401,
        })
        return
        }
        
        userStore.id = String(result.user.id)
        userStore.email = result.user.email
        userStore.username = result.user.username
        userStore.first_name = result.user.first_name
        userStore.last_name = result.user.last_name
        userStore.jwt = result.access_token
        localStorage.setItem('token', result.access_token)
        socket.connect()

        await router.push('/profile/edit')
    }
    notificationRef.value?.make_notification({
    error: {
        code: 'NETWORK_ERROR',
        message: error instanceof Error ? error.message : 'Error network',
    },
    status: 0,
    })
  }
})

</script>

<template>
    <form class="signup-form" @submit="onSubmit">
    <div class="field-group">
        <VeeField v-slot="{ componentField, errors }" name="email">
        <div class="field" :data-invalid="!!errors.length">
            <label for="signup-email">Email</label>
            <Input
                id="signup-email"
                v-bind="componentField"
                type="email"
                placeholder="exemple@domaine.com"
                :aria-invalid="!!errors.length"
            />
            <p v-if="errors.length" class="field-error">{{ errors[0] }}</p>
        </div>
        </VeeField>

        <VeeField v-slot="{ componentField, errors }" name="password">
        <div class="field" :data-invalid="!!errors.length">
            <label for="signup-password">Password</label>
            <Input
                id="signup-password"
                v-bind="componentField"
                type="password"
                placeholder="password"
                :aria-invalid="!!errors.length"
            />
            <p v-if="errors.length" class="field-error">{{ errors[0] }}</p>
        </div>
        </VeeField>

        <VeeField v-slot="{ componentField, errors }" name="pwd">
        <div class="field" :data-invalid="!!errors.length">
            <label for="signup-pwd">Confirm password</label>
            <Input
                id="signup-pwd"
                v-bind="componentField"
                type="password"
                placeholder="confirm password"
                :aria-invalid="!!errors.length"
            />
            <p v-if="errors.length" class="field-error">{{ errors[0] }}</p>
        </div>
        </VeeField>

        <VeeField v-slot="{ componentField, errors }" name="username">
        <div class="field" :data-invalid="!!errors.length">
            <label for="signup-username">Username</label>
            <Input
                id="signup-username"
                v-bind="componentField"
                type="text"
                placeholder="username"
                :aria-invalid="!!errors.length"
            />
            <p v-if="errors.length" class="field-error">{{ errors[0] }}</p>
        </div>
        </VeeField>

        <VeeField v-slot="{ componentField, errors }" name="first_name">
        <div class="field" :data-invalid="!!errors.length">
            <label for="signup-first-name">First name</label>
            <Input
                id="signup-first-name"
                v-bind="componentField"
                type="text"
                placeholder="John"
                :aria-invalid="!!errors.length"
            />
            <p v-if="errors.length" class="field-error">{{ errors[0] }}</p>
        </div>
        </VeeField>

        <VeeField v-slot="{ componentField, errors }" name="last_name">
        <div class="field" :data-invalid="!!errors.length">
            <label for="signup-last-name">Last name</label>
            <Input
                id="signup-last-name"
                v-bind="componentField"
                type="text"
                placeholder="Doe"
                autocomplete="family-name"
                :aria-invalid="!!errors.length"
            />
            <p v-if="errors.length" class="field-error">{{ errors[0] }}</p>
        </div>
        </VeeField>
        </div>

        <p v-if="formError" class="form-error" role="alert">{{ formError }}</p>

        <div class="form-actions">
        <button type="submit" :disabled="isSubmitting">Register</button>
        <button type="button" class="link" @click="router.push('/login')">
        Already have an account?
        </button>
        </div>
        </form>
</template>

<style scoped>

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 420px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.field label {
  font-size: 14px;
  font-weight: 600;
}

.field[data-invalid='true'] label {
  color: #d23b5a;
}

.field-error,
.form-error {
  margin: 0;
  color: #d23b5a;
  font-size: 13px;
}

.form-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

button.secondary,
button.link {
  background: transparent;
  border: 1px solid #f1e5e5;
  cursor: pointer;
}
</style>