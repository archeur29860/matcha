<script setup lang="ts">
import { ref } from 'vue';
import { block_user, remove_blocked_relation, get_user_blocked_by } from '@/services/api_blocked.ts';

const LIST_REF = ref({});

const user_id1 = ref("a924634f-42a9-4ab8-89ef-bf748f88ed57");
const user_id2 = ref("477f3a35-c5b2-4077-95e2-264faa1426e5");

async function block_user_id(){
    const response = await block_user(user_id1.value, user_id2.value);

    console.log(response)
    if (response?.data) {
        LIST_REF.value = response.data
    }
}

async function remove_blocked(){
    const response = await remove_blocked_relation(user_id1.value, user_id2.value);

    console.log(response)
    if (response?.data) {
        LIST_REF.value = response.data
    }
}

async function get_list_blocked_users(){
    const response = await get_user_blocked_by(user_id1.value);

    console.log(response)
    if (response?.data) {
        LIST_REF.value = response.data
    }
}
</script>

<template>
    <h1>BLOCKED TABLE</h1>
    <div class="border">
        <h2>Champs de requête:</h2>
        <p>user_id<input v-model="user_id1"/></p>
        <p>user_id_blocked<input v-model="user_id2"/></p>

        <button @click=block_user_id()>send</button>
        <button @click=remove_blocked()>remove</button>
    </div>
    <button @click=get_list_blocked_users()>GET users blocked by user_id</button>
     <h3>Résultat</h3>
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