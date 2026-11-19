<script setup lang="ts">
import { useRouter } from 'vue-router';
import Input from '@/components/input.vue';
import { useForm, Field, ErrorMessage } from 'vee-validate'
import { required } from '@vee-validate/rules'
import MultiSelect from '@/components/multiSelect.vue';
import SingleSelect from '@/components/singleSelect.vue';


const router = useRouter();

const { handleSubmit, values, isSubmitting } = useForm({
  initialValues: {
    email: '', password: '', pwd: '', username: '',
    first_name: '', last_name: '',
  },
})

function matchesPassword(value: unknown) {
  return value === values.password || "The passwords aren't matching"
}
const onSubmit = handleSubmit(async (form) => {
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

        if (!response.ok) {
            console.error('Erreur HTTP :', response.status, data);
            return;
        }

        console.log('Utilisateur créé :', data);

        // Redirection vers la connexion
        await router.push('/login');

    }
    catch (error: unknown) {
        console.error('error network :', error);
    }
})

</script>

<template>
    <form @submit.prevent="onSubmit">
        <label>Email</label>
        <Field name="email" rules="required|email|max:255" v-slot="{ field }">
            <Input v-model="field.value" type="email" placeholder="exemple@domaine.com" />
        </Field>
        <ErrorMessage name="email" class="field-error" />

        <label>Password</label>
        <Field name="password" rules="required|max:255" v-slot="{ field }">
            <Input v-model="field.value" type="password" 
            placeholder="password" />
        </Field>
        <ErrorMessage name="password" class="field-error" />

        <label>Confirm password</label>
        <Field name="pwd" rules="required|max:255" v-slot="{ field }">
            <Input v-model="field.value" type="password" 
            placeholder="confirm password" />
        </Field>
        <ErrorMessage name="pwd" class="field-error" />
        
        <label>Username</label>
        <Field name="username" rules="required|max:50|min:2" v-slot="{ field }">
            <Input v-model="field.value" type="text" placeholder="username" />
        </Field>
        <ErrorMessage name="username" class="field-error" />

        <label>First name</label>
        <Field name="first_name" rules="required|max:50|min:2" v-slot="{ field }">
            <Input v-model="field.value" type="text" placeholder="John" />
        </Field>
        <ErrorMessage name="first_name" class="field-error" />     

        <label>Last name</label>
        <Field name="last_name" rules="required|max:50|min:5" v-slot="{ field }">
            <Input v-model="field.value" type="text" placeholder="last name" />
        </Field>
        <ErrorMessage name="last_name" class="field-error" /> 

        <!-- v-if="!profile_completed" -->
        <button
            type="submit"
            :disabled="isSubmitting"
        >
            Register
        </button>

        <button type="button" @click="router.push('/login')">
            Already have an account?
        </button>
    </form>
</template>

<style scoped>

.field-error {
  display: block;
  margin: 4px 0 10px;
  color: #d23b5a;
  font-size: 13px;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style> 
