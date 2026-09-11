<script setup lang="ts">
import { ref } from 'vue';



const email = ref("");
const mail = ref({});
const password = ref('')
const username = ref('')
const last_name = ref('')
const first_name = ref('')

async function clicked() {
    console.log(email.value);
    try {
        const response = await fetch('http://localhost:5000/api/users/', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json',
            },
            body: JSON.stringify({
                email: email.value,
                username: username.value,
                last_name : last_name.value,
                first_name : first_name.value,
                password : password.value
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('Error HTTP:', response.status, data.error);
            return;
        }

        mail.value = data;
        console.log("Utilisateur créé :", mail.value);

    } catch (error) {
        console.error("Erreur réseau :", error);
    }
}
</script>

<template>
    <h1>MINOTTE TEST</h1>
    <p> email : 
        <input 
        type="email" 
        id="email" 
        name="add_email" 
        maxlength="25" 
        v-model="email" /> </p>
    <p> username : 
        <input 
        type="text" 
        id="username" 
        name="add_username" 
        maxlength="25" 
        v-model="username" /> </p>
    <p> last name : 
        <input 
        type="text" 
        id="last_name" 
        name="add_last_name" 
        maxlength="25" 
        v-model="last_name" /> </p>
    <p> first name : 
        <input 
        type="text" 
        id="first_name" 
        name="add_first_name" 
        maxlength="25" 
        v-model="first_name" /> </p>
    <p> password : 
        <input 
        type="password" 
        id="password" 
        name="add_password" 
        maxlength="25" 
        v-model="password" /> </p>
    <button @click=clicked()>send</button>

</template>