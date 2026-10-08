<script setup lang="ts">
import { ref } from 'vue'

import {
    block_user,
    remove_blocked_relation,
    get_user_blocked_by
} from '@/services/api_blocked.ts'

import Notification from '@/components/notification.vue'


// ---------------------------------------------------------------------------
// Notification
// ---------------------------------------------------------------------------

const notificationRef =
    ref<InstanceType<typeof Notification> | null>(null)


// ---------------------------------------------------------------------------
// Blocked users
// ---------------------------------------------------------------------------

const LIST_REF = ref<any[]>([])

const user_id1 = ref('')

const user_id2 = ref('')


// ---------------------------------------------------------------------------
// Block user
// ---------------------------------------------------------------------------

async function block_user_id() {
    const result = await block_user(
        user_id1.value,
        user_id2.value
    )

    console.log(result)

    // Notification
    notificationRef.value?.make_notification(result)

    // Données retournées par l'API
    if (result.success && result.data) {
        LIST_REF.value = result.data
    }
}


// ---------------------------------------------------------------------------
// Remove blocked relation
// ---------------------------------------------------------------------------

async function remove_blocked() {
    const result = await remove_blocked_relation(
        user_id1.value,
        user_id2.value
    )

    console.log(result)

    // Notification
    notificationRef.value?.make_notification(result)

    
    // Données retournées par l'API
    if (result.success && result.data) {
        LIST_REF.value = result.data
    }
}


// ---------------------------------------------------------------------------
// Get blocked users
// ---------------------------------------------------------------------------

async function get_list_blocked_users() {
    const result = await get_user_blocked_by(
        user_id1.value
    )
    
    console.log(result)
    
    // Notification
    notificationRef.value?.make_notification(result)
    
    // Données retournées par l'API
    if (result.success && result.data) {
        LIST_REF.value = result.data
    }
}
</script>


<template>

    <!-- Notification -->
    <Notification
        ref="notificationRef"
        :show="false"
        :duration="5000"
        position="bottom-left"
        :closable="true"
        :show-icon="true"
        width="400px"
        :z-index="10000"
    />


    <h1>BLOCKED TABLE</h1>


    <div class="border">

        <h2>Champs de requête:</h2>

        <p>
            user_id
            <input v-model="user_id1" />
        </p>

        <p>
            user_id_blocked
            <input v-model="user_id2" />
        </p>


        <button @click="block_user_id">
            send
        </button>

        <button @click="remove_blocked">
            remove
        </button>

    </div>


    <button @click="get_list_blocked_users">
        GET users blocked by user_id
    </button>


    <h3>Résultat</h3>


<div
    v-for="item in LIST_REF"
    :key="item.username"
    class="border"
>
    <p>
        {{item}}
    </p>
</div>

</template>


<style scoped>

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