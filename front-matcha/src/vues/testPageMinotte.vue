<script setup lang="ts">
import { ref } from 'vue';

const label = ref("");
const taglist = ref({});

async function clicked() {
    console.log(label.value);

    const response = await fetch('http://localhost:5000/api/tags/', {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
        },
        body: JSON.stringify({
            label: label.value,
        }),
    });

    const data = await response.json();

    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
        return;
    }

    taglist = await response.json();
}

async function get_list() {
    const response = await fetch('http://localhost:5000/api/tags/');

    const data = await response.json();

    if (!response.ok) {
        console.error("Erreur HTTP:", response.status, data.error);
        return;
    }

    taglist.value = data;
}

</script>

<template>
    <h1>MINOTTE TEST</h1>
    <p> TAG = 
        <input 
        type="text" 
        id="add_tag_id" 
        name="add_tag_name" 
        maxlength="25" 
        v-model="label" /> </p>
    <button @click=clicked()>send</button>

    <button @click=get_list()>getlist</button>
    <div v-for="tag in taglist"><p>{{tag}}</p></div>
</template>