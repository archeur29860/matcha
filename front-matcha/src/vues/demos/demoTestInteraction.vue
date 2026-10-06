<script setup lang="ts">
import { ref } from 'vue';
import { new_iteraction, get_list_interaction_from, get_list_interaction_to } from '@/services/api_interaction';

const LIST_REF = ref({});

const user_id1 = ref("cc7cbee6-166d-478f-9224-430fe114d36c");
const user_id2 = ref("f45281fe-8f39-4019-929a-20510970389e");
const status = ref("Liked")

async function create_inter(){
    const response = await new_iteraction(user_id1.value, user_id2.value, status.value);

    console.log(response)
    LIST_REF.value = response.data;
}

async function get_list_from(){
    const response = await get_list_interaction_from(user_id1.value);

    console.log(response)
    LIST_REF.value = response.data.items
}

async function get_list_to(){
    const response = await get_list_interaction_to(user_id2.value);

    console.log(response)
    LIST_REF.value = response.data.items
}
</script>

<template>
    <h1>INTERACTION TABLE</h1>
    <div class="border">
        <h2>Champs de requête:</h2>
        <p>from_user_id<input v-model="user_id1"/></p>
        <p>to_user_id<input v-model="user_id2"/></p>
        <p>type of interaction
            <select v-model="status">
                <option value="Liked">Liked</option>
                <option value="Viewed">Viewed</option>
                <option value="Matched">Matched</option>
            </select>
        </p>
        <button @click=create_inter()>send</button>
    </div>
    <button @click=get_list_from()>GET FROM</button>
    <button @click=get_list_to()>GET TO</button>
    <!-- <button @click=delete_item()>delete</button> -->
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