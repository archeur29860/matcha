<script setup lang="ts">
const props = defineProps<{
    user_id: string
    username: string
}>()

const emit = defineEmits<{
    (e: 'user-click', user_id: string): void
}>()

function handleClick() {
    emit('user-click', props.user_id)
    console.log('emit:', props.user_id)
}
</script>

<template>
    <button
        type="button"
        class="user-clickable"
        @click="handleClick"
    >
        <span class="username">
            {{ props.username }}
        </span>
    </button>
</template>

<style scoped>
.user-clickable {
    display: inline-flex;
    align-items: center;
    max-width: 100%;

    padding: 0.4rem 0.75rem;

    border: none;
    border-radius: 0.5rem;

    background: transparent;
    color: #d4a373;

    font: inherit;
    font-weight: 600;

    cursor: pointer;

    transition:
        background-color 0.15s ease,
        color 0.15s ease;
}

.user-clickable:hover {
    background-color: #e9edc9;
    color: #d4a373;
}

.user-clickable:focus-visible {
    outline: 2px solid #020202;
    outline-offset: 2px;
}

.username {
    max-width: 100%;

    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Mobile */
@media (max-width: 600px) {
    .user-clickable {
        width: 100%;
        justify-content: flex-start;

        padding: 0.6rem 0.75rem;

        font-size: 0.95rem;
    }
}
</style>
