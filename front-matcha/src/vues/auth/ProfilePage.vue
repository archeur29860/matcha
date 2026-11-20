<!-- 
<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useForm, Field, ErrorMessage } from 'vee-validate'
import { required } from '@vee-validate/rules'

import Input from '@/components/input.vue'
import MultiSelect from '@/components/multiSelect.vue'
import SingleSelect from '@/components/singleSelect.vue'

const router = useRouter()

const { handleSubmit, values, isSubmitting } = useForm({
    initialValues: {
        email: '', password: '', pwd: '', username: '',
        first_name: '', last_name: '', age: '', gender: 'Other',
        gender_pref: ['Male', 'Female'], bio: '',
    }, 
})
// picture_profile_index: '', localisation: '', tags: '',

function matchesPassword(value: unknown) {
  return value === values.password || "The passwords aren't matching"
}
const onSubmit = handleSubmit(async (form) => {
    try {
        const response = await fetch('http://localhost:5000/api/users/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
            email: form.email.trim(),
            username: form.username.trim(),
            first_name: form.first_name.trim(),
            last_name: form.last_name.trim(),
            password: form.password,
            age: form.age || null,
            gender: form.gender,
            gender_pref: form.gender_pref,
            bio: form.bio,
            }  catch (error: unknown) {
                notificationRef.value?.make_notification({
                    error: {
                        code: 'NETWORK_ERROR',
                        message: error instanceof Error ? error.message : 'Error network',
                    },
                    status: 0,
                })
            }
        })
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
    <Field name="email" rules="required|email|max:255" v-slot="{ componentField }">
        <Input v-bind="componentField" type="email" placeholder="exemple@domaine.com" />
    </Field>
    <ErrorMessage name="email" class="field-error" />

    <label>Password</label>
    <Field name="password" rules="required|max:255" v-slot="{ componentField }">
        <Input v-bind="componentField" type="password" placeholder="password" />
    </Field>
    <ErrorMessage name="password" class="field-error" />

    <label>Confirm password</label>
    <Field name="pwd" :rules="[required, matchesPassword]" v-slot="{ componentField }">
        <Input v-bind="componentField" type="password" placeholder="confirm password" />
    </Field>
    <ErrorMessage name="pwd" class="field-error" />

    <label>Username</label>
    <Field name="username" rules="required|max:50|min:2" v-slot="{ componentField }">
        <Input v-bind="componentField" type="text" placeholder="username" />
    </Field>
    <ErrorMessage name="username" class="field-error" />

    <label>First name</label>
    <Field name="first_name" rules="required|max:50|min:3" v-slot="{ componentField }">
        <Input v-bind="componentField" type="text" placeholder="John" />
    </Field>
    <ErrorMessage name="first_name" class="field-error" />

    <label>Last name</label>
    <Field name="last_name" rules="required|max:50|min:3" v-slot="{ componentField }">
        <Input v-bind="componentField" type="text" placeholder="last name" />
    </Field>
    <ErrorMessage name="last_name" class="field-error" />

    <label>Birthday</label>
    <Field name="age" rules="required|min_age:18" v-slot="{ componentField }">
        <Input v-bind="componentField" type="date" placeholder="birthday" />
    </Field>
    <ErrorMessage name="age" class="field-error" />

    <label>Gender</label>
    <Field name="gender" rules="required|one_of:Male,Female,Other" v-slot="{ componentField }">
        <SingleSelect v-bind="componentField" />
    </Field>
    <ErrorMessage name="gender" class="field-error" />

    <label>Gender preferences</label>
    <Field name="gender_pref" rules="required|one_of:Male,Female,Other" v-slot="{ componentField }">
        <MultiSelect v-bind="componentField" />
    </Field>
    <ErrorMessage name="gender_pref" class="field-error" />

    <label>Bio</label>
    <Field name="bio" rules="required|max:2000|min:20" v-slot="{ field }">
        <textarea v-bind="field" placeholder="about you"></textarea>
    </Field>
    <ErrorMessage name="bio" class="field-error" />



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
</style> -->

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import FormUser from '@/components/formUser.vue'

const formRef = ref<InstanceType<typeof FormUser> | null>(null)
const router = useRouter()
</script>
<template>
    <FormUser/>
    <button type="button" @click="modifyProfile">
            Modify
        </button> 
</template>