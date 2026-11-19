
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import InteractionCard from '../components/interactionCard.vue'

import {
  get_list_interaction_to,
  get_list_interaction_from
} from '@/services/api_interaction'

import { useUserStore } from '@/stores/user'
import type { Interaction } from '@/types/interaction'
import { handleClickOnProfile } from '@/composable/useNavigation'

const userStore = useUserStore()

const inter_to_me = ref<Interaction[]>([])
const inter_from_me = ref<Interaction[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [result_to, result_from] = await Promise.all([
      get_list_interaction_to(userStore.id),
      get_list_interaction_from(userStore.id)
    ])

    if (result_to) {
      inter_to_me.value = result_to
    }

    if (result_from) {
      inter_from_me.value = result_from
    }

  } catch (error) {
    console.error('Erreur chargement interactions:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main class="interactions-page">

    <header class="page-header">
      <h1>Mes interactions</h1>
      <p>Retrouvez les interactions avec les autres profils.</p>
    </header>

    <div class="list-container">

      <!-- Interactions reçues -->
      <section class="interaction-list">
        <header class="list-header">
          <div>
            <h2>Interactions reçues</h2>
            <span class="list-count">
              {{ inter_to_me.length }} interactions
            </span>
          </div>
        </header>

        <div class="list-content">

          <div v-if="loading" class="empty-state">
            Chargement...
          </div>

          <div
            v-else-if="inter_to_me.length === 0"
            class="empty-state"
          >
            Aucune interaction reçue pour le moment.
          </div>

          <InteractionCard
            v-for="interaction in inter_to_me"
            :key="interaction.id"
            :from_username="interaction.username"
            :user_id="interaction.user_id"
            :type-of-inter="interaction.typeOfInter"
            :created_at="interaction.created_at"
            @clickOnProfile="handleClickOnProfile"
          />

        </div>
      </section>

      <!-- Interactions envoyées -->
      <section class="interaction-list">
        <header class="list-header">
          <div>
            <h2>Interactions envoyées</h2>
            <span class="list-count">
              {{ inter_from_me.length }} interactions
            </span>
          </div>
        </header>

        <div class="list-content">

          <div v-if="loading" class="empty-state">
            Chargement...
          </div>

          <div
            v-else-if="inter_from_me.length === 0"
            class="empty-state"
          >
            Vous n'avez pas encore interagi avec des profils.
          </div>

          <InteractionCard
            v-for="interaction in inter_from_me"
            :key="interaction.id"
            :to_username="interaction.username"
            :user_id="interaction.user_id"
            :type-of-inter="interaction.typeOfInter"
            :created_at="interaction.created_at"
            @clickOnProfile="handleClickOnProfile"
          />

        </div>
      </section>

    </div>
  </main>
</template>

<style scoped>

/* =========================
   PAGE
========================= */

.interactions-page {
  width: 100%;
  min-height: 100vh;
  padding: 28px;
  box-sizing: border-box;
  background: #fffafb;
}

/* =========================
   TITRE
========================= */

.page-header {
  text-align: center;
  margin-bottom: 28px;
}

.page-header h1 {
  margin: 0;
  color: #e86f8d;
  font-size: clamp(24px, 3vw, 34px);
  font-weight: 700;
}

.page-header p {
  color: #a7768b;
  font-size: 14px;
  margin-top: 8px;
}

/* =========================
   CONTENEUR DES LISTES
========================= */

.list-container {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
  gap: 24px;
  width: 100%;
  max-width: 1500px;
  margin: 0 auto;
}

/* =========================
   LISTES
========================= */

.interaction-list {
  min-width: 0;
  height: min(75vh, 850px);
  display: flex;
  flex-direction: column;

  background: #ffffff;
  border: 1px solid #f1e5e5;
  border-radius: 20px;
  box-shadow: 0 5px 18px rgba(60, 30, 40, 0.05);

  overflow: hidden;
}

/* =========================
   HEADER DES LISTES
========================= */

.list-header {
  position: sticky;
  top: 0;
  z-index: 2;
  flex-shrink: 0;

  padding: 18px 20px;
  background: #ffffff;
  border-bottom: 1px solid #f1e5e5;
}

.list-header h2 {
  margin: 0;
  color: #302329;
  font-size: 18px;
  font-weight: 600;
}

.list-count {
  display: block;
  margin-top: 5px;
  color: #a7768b;
  font-size: 12px;
}

/* =========================
   CONTENU SCROLLABLE
========================= */

.list-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  overflow-x: hidden;

  display: flex;
  flex-direction: column;
  gap: 12px;

  padding: 16px;
  overscroll-behavior-y: contain;

  scrollbar-width: thin;
  scrollbar-color: #e8c4ce transparent;
}

.list-content > * {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

/* Scrollbar Chrome / Safari */

.list-content::-webkit-scrollbar {
  width: 6px;
}

.list-content::-webkit-scrollbar-thumb {
  background: #e8c4ce;
  border-radius: 10px;
}

.list-content::-webkit-scrollbar-thumb:hover {
  background: #ed6284;
}

/* =========================
   ÉTATS VIDES
========================= */

.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 140px;

  padding: 20px;
  color: #a7768b;
  font-size: 14px;
  text-align: center;
}

/* =========================
   TABLETTES
========================= */

@media (max-width: 900px) {
  .interactions-page {
    padding: 20px;
  }

  .list-container {
    gap: 16px;
  }

  .interaction-list {
    height: 70vh;
  }

  .list-content {
    padding: 12px;
  }

  .list-header {
    padding: 16px;
  }
}

/* =========================
   MOBILES
========================= */

@media (max-width: 650px) {
  .interactions-page {
    padding: 16px 10px;
  }

  .page-header {
    margin-bottom: 20px;
  }

  .list-container {
    grid-template-columns: minmax(0, 1fr);
    gap: 20px;
  }

  .interaction-list {
    width: 100%;
    height: 65vh;
    min-height: 350px;
    border-radius: 16px;
  }

  .list-header {
    padding: 14px;
  }

  .list-header h2 {
    font-size: 16px;
  }

  .list-content {
    padding: 10px;
    gap: 10px;
  }
}

/* =========================
   PETITS MOBILES
========================= */

@media (max-width: 380px) {
  .interactions-page {
    padding: 12px 8px;
  }

  .interaction-list {
    min-height: 300px;
    height: 60vh;
  }

  .page-header p {
    font-size: 13px;
  }
}

</style>
