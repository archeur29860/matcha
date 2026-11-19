
<script setup lang="ts">
import { ref } from 'vue'
import SituGeo from '@/components/situgeo.vue'

// À remplacer par ton système de gestion utilisateur


// Mode du composant
const mode = ref<'create' | 'update'>('create')

// Résultat de l'enregistrement
const savedLocation = ref<any>(null)
const message = ref('')

function handleLocationSaved(data: any) {
  savedLocation.value = data
  message.value = 'Ta localisation a été enregistrée avec succès !'

  console.log('Localisation enregistrée :', data)
}

// Changement de mode
function changeMode(newMode: 'create' | 'update') {
  mode.value = newMode
  message.value = ''
  savedLocation.value = null
}
</script>

<template>
  <main class="page">

    <header class="page-header">
      <h1>Gestion de ma localisation</h1>
      <p>
        Configure ta situation géographique pour Matcha.
      </p>
    </header>

    <!-- Choix du mode -->

    <div class="mode-selector">
      <button
        :class="{ active: mode === 'create' }"
        @click="changeMode('create')"
      >
        Nouvelle localisation
      </button>

      <button
        :class="{ active: mode === 'update' }"
        @click="changeMode('update')"
      >
        Modifier ma localisation
      </button>
    </div>

    <!-- Composant enfant -->

    <SituGeo
      :key="mode"
      :mode="mode"
      @saved="handleLocationSaved"
    />

    <!-- Résultat -->

    <section v-if="savedLocation" class="saved-result">
      <h2>Localisation enregistrée</h2>

      <p>{{ message }}</p>

      <pre>{{ JSON.stringify(savedLocation, null, 2) }}</pre>
    </section>

  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  padding: 30px 20px;
  background: #fff7f9;
  box-sizing: border-box;
}

.page-header {
  text-align: center;
  margin-bottom: 25px;
}

.page-header h1 {
  color: #38252c;
}

.page-header p {
  color: #987f87;
}

.mode-selector {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.mode-selector button {
  padding: 12px 20px;
  border: 1px solid #e77b9a;
  border-radius: 12px;
  background: white;
  color: #b85570;
  font-weight: 600;
  cursor: pointer;
}

.mode-selector button.active {
  background: #e77b9a;
  color: white;
}

.saved-result {
  max-width: 600px;
  margin: 25px auto;
  padding: 20px;
  border-radius: 16px;
  background: white;
  border: 1px solid #f5dce3;
}

.saved-result h2 {
  color: #b85570;
}

.saved-result p {
  color: #287a52;
}

.saved-result pre {
  overflow-x: auto;
  padding: 12px;
  border-radius: 8px;
  background: #fff4f7;
  font-size: 12px;
}
</style>
