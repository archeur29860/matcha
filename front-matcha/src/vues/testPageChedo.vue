<script setup lang="ts">

import user_clickable from '@/components/user_clickable.vue';

function catch_emit(user_id:string){
    console.log('catch:', user_id)
}

</script>

<template>
    <user_clickable user_id="132" username="usernameTest" @user-click="catch_emit"/>
</template>

<style scoped>
</style>