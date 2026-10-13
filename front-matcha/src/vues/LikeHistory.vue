
<script setup lang="ts">
import { onMounted } from 'vue';
import InteractionCard from '../components/interactionCard.vue'
import { get_list_interaction_to } from '@/services/api_interaction.ts';
import { useUserStore } from '@/stores/user.ts';

const userStore = useUserStore()

onMounted( async () => {
    const result = await get_list_interaction_to(userStore.id)
})


const interactions = [
  {
    id: 1,
    from_username: 'Alice',
    to_username: 'You',
    typeOfInter: 'Like',
    created_at: '2026-10-13T10:30:00',
  },
  {
    id: 2,
    from_username: 'Bob',
    to_username: 'You',
    typeOfInter: 'Visite de profil',
    created_at: '2026-10-12T16:45:00',
  },
]
</script>

<template>
  <div class="interaction-list">
    <InteractionCard
      v-for="interaction in interactions"
      :key="interaction.id"
      :from_username="interaction.from_username"
      :to_username="interaction.to_username"
      :type-of-inter="interaction.typeOfInter"
      :created_at="interaction.created_at"
    />
  </div>
</template>

<style scoped>
.interaction-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}
</style>
