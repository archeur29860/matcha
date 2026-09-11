<script setup lang="ts">
import { ref } from 'vue';

const URLAPI = "blocked"
const LIST_REF = ref({});

const user_id = ref("");
const user_id_blocked = ref("");

async function post_body() {

    const response = await fetch(`http://localhost:5000/api/${URLAPI}/`, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
        },
        body: JSON.stringify({
            user_id: user_id.value,
            user_id_blocked: user_id_blocked.value,
        }),
    });

    const data = await response.json();
    
    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
        return;
    }
    
    LIST_REF.value = data;
    console.log(data)
}

async function get_list() {
    const response = await fetch(`http://localhost:5000/api/${URLAPI}/`);

    const data = await response.json();

    if (!response.ok) {
        console.error("Erreur HTTP:", response.status, data.error);
        return;
    }

    LIST_REF.value = data;
}


async function delete_item() {
    try {
        const response = await fetch(
            `http://localhost:5000/api/${URLAPI}/`,
            {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user_id: user_id.value,
                    user_id_blocked: user_id_blocked.value,
                }),
            }
        );

        const data = await response.json();

        if (!response.ok) {
            console.error("Erreur :", data.error);
            return;
        }

        console.log("Blocage supprimé :", data);

    } catch (error) {
        console.error("Erreur réseau :", error);
    }
}

</script>

<template>
    <h1>CHEDO TEST</h1>
    <div class="border">
        <h2>POST {{ URLAPI }}</h2>
        FORM
        <p>user_id<input v-model="user_id"/></p>
        <p>user_id_blocked<input v-model="user_id_blocked"/></p>
        <button @click=post_body()>send</button>
    </div>
    <button @click=get_list()>GET ALL</button>
    <button @click=delete_item()>delete</button>
    <div v-for="item in LIST_REF" class="border"><p>=>{{item}}</p></div>
</template>

<style lang="css" scoped>
.container {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    -ms-flex-align: center;
}
.border {
    border: 0.2rem solid;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}
</style>