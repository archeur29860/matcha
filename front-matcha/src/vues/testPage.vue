<script setup lang="ts">
import { ref } from 'vue';

const label = ref("");

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
}

</script>

<template>
    <p> TAG = 
        <input 
        type="text" 
        id="add_tag_id" 
        name="add_tag_name" 
        maxlength="25" 
        v-model="label" /> </p>
    <button @click=clicked()>send</button>
</template>