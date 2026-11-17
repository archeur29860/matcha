
<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import Input from '@/components/input.vue';

const router = useRouter();

const email = ref('');
const password = ref('');
const password1 = ref('');
const username = ref('');
const first_name = ref('');
const last_name = ref('');
const age = ref('');
const gender = ref('Other');
const gender_pref = ref<string[]>(['Male', 'Female']);
const bio = ref('');
const picture_profile_index = ref('');
const localisation = ref('');
const tags = ref('');

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


const isValidEmail = computed(() =>
    emailRegex.test(email.value)
);

const isFormValid = computed(() =>
    isValidEmail.value &&
    password.value.trim() !== '' &&
    password.value.trim() == password1.value.trim() &&
    username.value.trim() !== '' &&
    first_name.value.trim() !== '' &&
    last_name.value.trim() !== '' &&
    age.value.trim() !== '' &&
    gender.value.trim() !== '' &&
    gender_pref.value.length > 0 &&
    bio.value.trim() !== '' &&
    picture_profile_index.value.trim() !== '' &&
    localisation.value.trim() !== '' &&
    tags.value.trim() !== ''
);

async function handleclick() {
    if (!isFormValid.value) return;

    try {
        const response = await fetch(
            'http://localhost:5000/api/users/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email.value.trim(),
                    username: username.value.trim(),
                    first_name: first_name.value.trim(),
                    last_name: last_name.value.trim(),
                    password: password.value,
                    age: age.value || null,
                    gender: gender.value,
                    gender_pref: gender_pref.value,
                    bio: bio.value,
                    picture_profile_index:
                        picture_profile_index.value === ''
                            ? nullpicture_profile
                            : Number(picture_profile_index.value),
                    localisation: localisation.value || null,
                    tags: tags.value
                        .split(',')
                        .map(tag => tag.trim())
                        .filter(Boolean)
                        .map(Number),
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

    } catch (error: unknown) {
        console.error('Erreur réseau :', error);
    }
}
</script>

<template>
    <form @submit.prevent="handleclick">
        <div :class="{ 'email-invalid': email && !isValidEmail }">
            <Input
                v-model="email"
                type="email"
                placeholder="exemple@domaine.com"
            />
        </div>

        <Input
            v-model="password"
            type="password"
            placeholder="password"
        />

        <Input
            v-model="password1"
            type="password"
            placeholder="confirm password"
        />

        <Input
            v-model="username"
            type="text"
            placeholder="username"
        />

        <Input
            v-model="first_name"
            type="text"
            placeholder="Jonh"
        />

        <Input
            v-model="last_name"
            type="text"
            placeholder="Doe"
        />

        <Input
            v-model="age"
            type="date"
            placeholder="birthday"
        />

        <label for="gender">Genre</label>
        <select id="gender" v-model="gender">
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
        </select>

        <label for="gender_pref">Genres preference</label>
        <select id="gender_pref" v-model="gender_pref" multiple>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
        </select>

        <label for="bio">Bio</label>
        <textarea
            id="bio"
            v-model="bio"
            placeholder="about you"
        >
        </textarea>
        <Input
            v-model="picture_profile_index"
            type="number"
            placeholder="Index of the picture"
        />

        <Input
            v-model="localisation"
            type="text"
            placeholder="Localisation"
        />

        <Input
            v-model="tags"
            type="text"
            placeholder="Interest(1, 2, 3)"
        />


        <button
            v-if="!profile_completed"
            type="submit"
            :disabled="!isFormValid"
        >
            Register
        </button>

        <button
            v-else
            type="button"
            @click="modifyProfile"
        >
            Modify
        </button>


        <button type="button" @click="router.push('/login')">
            Already have an account?
        </button>
    </form>
</template>

<style scoped>
.email-invalid {
    border: 1px solid red;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
</style>
