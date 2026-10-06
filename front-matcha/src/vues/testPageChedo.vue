<script setup lang="ts">
import { ref } from 'vue';
import { new_iteraction, get_list_interaction_from, get_list_interaction_to } from '@/services/api_interaction';

const URLAPI = "interaction"
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
// async function post_body() {

//     const response = await fetch(`http://localhost:5000/api/${URLAPI}/`, {
//         method: 'POST',
//         headers: {
//             'Content-Type':'application/json',
//         },
//         body: JSON.stringify({
//             from_user_id: user_id1.value,
//             to_user_id: user_id2.value,
//             which_interaction: status.value,
//         }),
//     });

//     const data = await response.json();
    
//     if (!response.ok) {
//         console.error('Erreur HTTP:', response.status, data.error);
//         return;
//     }
    
//     LIST_REF.value = data.data;
//     console.log(data)
// }

// async function get_list1() {
//     const response = await fetch(`http://localhost:5000/api/${URLAPI}/from/${user_id1.value}/`);

//     const data = await response.json();

//     if (!response.ok) {
//         console.error("Erreur HTTP:", response.status, data.error);
//         return;
//     }

//     LIST_REF.value = data.data.items;
//     console.log(data)
// }

// async function get_list2() {
//     const response = await fetch(`http://localhost:5000/api/${URLAPI}/to/${user_id1.value}/`);

//     const data = await response.json();

//     if (!response.ok) {
//         console.error("Erreur HTTP:", response.status, data.error);
//         return;
//     }

//     LIST_REF.value = data.data.items;
//     console.log(data)
// }

// async function delete_item() {
//     try {
//         const response = await fetch(
//             `http://localhost:5000/api/${URLAPI}/`,
//             {
//                 method: "DELETE",
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body: JSON.stringify({
//                     user_id: user_id.value,
//                     user_id_blocked: user_id_blocked.value,
//                 }),
//             }
//         );

//         const data = await response.json();

//         if (!response.ok) {
//             console.error("Erreur :", data.error);
//             return;
//         }

//         console.log("Blocage supprimé :", data);

//     } catch (error) {
//         console.error("Erreur réseau :", error);
//     }
// }

</script>

<template>
    <h1>CHEDO TEST</h1>
    <div class="border">
        <h2>POST {{ URLAPI }}</h2>
        FORM
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