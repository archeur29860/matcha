
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import InteractionCard from '../components/interactionCard.vue'
import { get_list_interaction_to } from '@/services/api_interaction.ts';
import { useUserStore } from '@/stores/user.ts';
import type { Interaction } from '@/types/interaction.ts';

const userStore = useUserStore()

const likes = ref<Interaction[]>([])

onMounted( async () => {
    const result = await get_list_interaction_to(userStore.id)

    if (result){
      likes.value = result
    }
})

</script>


<template>
  <div class="list-container">
    <!-- Première liste -->
    <div class="interaction-list">
      <h2>Interactions reçues</h2>

      <InteractionCard
        v-for="interaction in likes"
        :key="interaction.id"
        :from_username="interaction.username"
        :type-of-inter="interaction.typeOfInter"
        :created_at="interaction.created_at"
      />
    </div>

    <!-- Deuxième liste -->
    <div class="interaction-list">
      <h2>Interactions envoyées</h2>

      <InteractionCard
        v-for="interaction in likes"
        :key="interaction.id"
        :from_username="interaction.username"
        :type-of-inter="interaction.typeOfInter"
        :created_at="interaction.created_at"
      />
    </div>
  </div>
</template>


<style scoped>

.list-container {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 24px;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

/* Chaque liste possède son propre scroll */
.interaction-list {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  height: 90vh;
  overflow-y: auto;
  overflow-x: hidden;
  gap: 12px;

  padding: 16px;
  box-sizing: border-box;

  background: #ffffff;
  border: 1px solid #f1e5e5;
  border-radius: 20px;
  box-shadow: 0 5px 18px rgba(60, 30, 40, 0.05);

  scrollbar-width: thin;
  scrollbar-color: #e8c4ce transparent;
  overscroll-behavior-y: contain;
}

/* Titre toujours visible pendant le scroll */
.interaction-list h2 {
  position: sticky;
  top: -16px;
  z-index: 2;

  flex-shrink: 0;
  margin: -16px -16px 8px;
  padding: 16px;

  color: #302329;
  background: #ffffff;
  border-bottom: 1px solid #f1e5e5;
  font-size: 18px;
  font-weight: 600;
}

/* Barre de scroll pour Chrome, Edge et Safari */
.interaction-list::-webkit-scrollbar {
  width: 6px;
}

.interaction-list::-webkit-scrollbar-track {
  background: transparent;
}

.interaction-list::-webkit-scrollbar-thumb {
  background: #e8c4ce;
  border-radius: 10px;
}

.interaction-list::-webkit-scrollbar-thumb:hover {
  background: #ed6284;
}

/* Les cartes occupent la largeur disponible */
.interaction-list > * {
  max-width: 100%;
  box-sizing: border-box;
}

/* Adaptation aux tablettes et téléphones */
@media (max-width: 768px) {
  .list-container {
    flex-direction: column;
    gap: 20px;
    padding: 12px;
  }

  .interaction-list {
    flex: none;
    width: 100%;
    height: 100%;
    padding: 12px;
    border-radius: 16px;
  }

  .interaction-list h2 {
    top: -12px;
    margin: -12px -12px 8px;
    padding: 12px;
    font-size: 16px;
  }
}

/* Petits écrans */
@media (max-width: 480px) {
  .list-container {
    padding: 8px;
    gap: 16px;
  }

  .interaction-list {
    /* height: 45vh; */
    gap: 10px;
  }
}

</style>
