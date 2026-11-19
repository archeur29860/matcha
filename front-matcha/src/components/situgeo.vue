
<script setup lang="ts">
import { ref } from 'vue'
import { create_situgeo, update_situgeo } from '@/services/api_situgeo'
import { useUserStore } from '@/stores/user'

// Props
const props = defineProps<{
  mode: 'create' | 'update'
}>()

const emit = defineEmits<{
  (e: 'saved', data: any): void
}>()

// Pinia Store
const userStore = useUserStore()

// States
const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)

const city = ref('')
const gpsConsent = ref(false)

const loading = ref(false)
const saving = ref(false)

const error = ref<string | null>(null)
const successMessage = ref<string | null>(null)
const permission = ref('Non demandée')

// Récupération GPS
function getCurrentLocation() {
  if (!gpsConsent.value) {
    error.value = "Tu dois accepter l'utilisation du GPS."
    return
  }

  if (!navigator.geolocation) {
    error.value = "La géolocalisation n'est pas supportée."
    return
  }

  loading.value = true
  error.value = null
  successMessage.value = null
  permission.value = 'En attente...'

  navigator.geolocation.getCurrentPosition(
    (position) => {
      latitude.value = position.coords.latitude
      longitude.value = position.coords.longitude

      loading.value = false
      permission.value = 'Autorisée'
      error.value = null
    },
    (err) => {
      loading.value = false

      switch (err.code) {
        case err.PERMISSION_DENIED:
          permission.value = 'Refusée'
          error.value = "Tu as refusé l'accès à ta position."
          break

        case err.POSITION_UNAVAILABLE:
          error.value = 'Position GPS indisponible.'
          break

        case err.TIMEOUT:
          error.value = 'Le délai de recherche GPS est dépassé.'
          break

        default:
          error.value = 'Une erreur GPS est survenue.'
      }
    },
    {
      enableHighAccuracy: true,
      timeout: 15000,
      maximumAge: 0,
    }
  )
}

// Enregistrement de la localisation
async function saveLocation() {
  error.value = null
  successMessage.value = null

  // Récupération de l'identifiant depuis Pinia
  if (!userStore.id) {
    error.value = 'Identifiant utilisateur manquant.'
    return
  }

  const hasGPS = latitude.value !== null && longitude.value !== null
  const hasCity = city.value.trim().length > 0

  if (!hasGPS && !hasCity) {
    error.value = 'Récupère ta position GPS ou renseigne une ville.'
    return
  }

  if (hasGPS && !gpsConsent.value) {
    error.value = 'Le consentement GPS est nécessaire.'
    return
  }

  saving.value = true

  try {
    let data

    if (props.mode === 'update') {
      data = await update_situgeo(
        userStore.id,
        hasGPS,
        hasGPS ? latitude.value! : undefined,
        hasGPS ? longitude.value! : undefined,
        hasGPS ? undefined : city.value.trim()
      )
    } else {
      data = await create_situgeo(
        userStore.id,
        hasGPS,
        hasGPS ? latitude.value! : undefined,
        hasGPS ? longitude.value! : undefined,
        hasGPS ? undefined : city.value.trim()
      )
    }

    if (!data) {
      throw new Error("L'enregistrement de la localisation a échoué.")
    }

    successMessage.value = 'Ta localisation a bien été enregistrée !'

    emit('saved', data)

  } catch (err) {
    error.value = err instanceof Error
      ? err.message
      : "Une erreur est survenue lors de l'enregistrement."
  } finally {
    saving.value = false
  }
}

// Réinitialisation GPS si consentement retiré
function handleConsentChange() {
  if (!gpsConsent.value) {
    latitude.value = null
    longitude.value = null
    permission.value = 'Non demandée'
  }

  error.value = null
}
</script>

<template>
  <main class="geo-page">
    <section class="geo-card">

      <header class="geo-header">
        <span class="geo-icon">📍</span>

        <h1>Ma localisation</h1>

        <p>
          Indique ta position pour profiter pleinement de Matcha.
        </p>
      </header>

      <!-- Consentement GPS -->
      <div class="consent-box">
        <label class="consent-label">
          <input
            v-model="gpsConsent"
            type="checkbox"
            @change="handleConsentChange"
          />

          <span>
            J'accepte de partager ma position GPS.
          </span>
        </label>

        <small>
          Tu peux également renseigner ta ville manuellement.
        </small>
      </div>

      <!-- Permission -->
      <div class="permission">
        <span>Autorisation GPS</span>
        <strong>{{ permission }}</strong>
      </div>

      <!-- GPS -->
      <div class="geo-actions">
        <button
          class="geo-button"
          :disabled="loading || saving || !gpsConsent"
          @click="getCurrentLocation"
        >
          {{ loading ? 'Recherche...' : 'Obtenir ma position GPS' }}
        </button>
      </div>

      <!-- GPS coordinates -->
      <div
        v-if="latitude !== null && longitude !== null"
        class="coordinates"
      >
        <h2>Position récupérée</h2>

        <div class="result-row">
          <span>Latitude</span>
          <strong>{{ latitude.toFixed(6) }}</strong>
        </div>

        <div class="result-row">
          <span>Longitude</span>
          <strong>{{ longitude.toFixed(6) }}</strong>
        </div>

        <a
          :href="`https://www.google.com/maps?q=${latitude},${longitude}`"
          target="_blank"
          rel="noopener noreferrer"
          class="maps-link"
        >
          Voir ma position sur Google Maps ↗
        </a>
      </div>

      <!-- Manual city -->
      <div class="manual-location">
        <h2>Ou renseigner une ville</h2>

        <input
          v-model="city"
          type="text"
          placeholder="Ex : Paris, Lyon, Marseille..."
          :disabled="saving"
        />

        <p>
          Cette option permet d'enregistrer ta localisation sans utiliser
          le GPS.
        </p>
      </div>

      <!-- Errors -->
      <div v-if="error" class="geo-error">
        {{ error }}
      </div>

      <!-- Success -->
      <div v-if="successMessage" class="geo-success">
        {{ successMessage }}
      </div>

      <!-- Save -->
      <button
        class="save-button"
        :disabled="saving || loading"
        @click="saveLocation"
      >
        {{
          saving
            ? 'Enregistrement...'
            : mode === 'update'
              ? 'Modifier ma localisation'
              : 'Enregistrer ma localisation'
        }}
      </button>

      <p class="geo-info">
        Tes informations de localisation sont utilisées conformément
        à ton consentement.
      </p>

    </section>
  </main>
</template>

<style scoped>
.geo-page {
  min-height: 100vh;
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  background: #fff7f9;
  box-sizing: border-box;
}

.geo-card {
  width: 100%;
  max-width: 600px;
  padding: 32px;
  border: 1px solid #f5dce3;
  border-radius: 24px;
  background: white;
  box-shadow: 0 12px 35px rgba(120, 50, 75, 0.08);
  box-sizing: border-box;
}

.geo-header {
  text-align: center;
  margin-bottom: 28px;
}

.geo-icon {
  font-size: 42px;
}

.geo-header h1 {
  margin: 12px 0 8px;
  color: #38252c;
  font-size: 26px;
}

.geo-header p {
  color: #987f87;
  font-size: 14px;
}

.consent-box {
  padding: 16px;
  border-radius: 12px;
  background: #fff4f7;
  color: #795765;
}

.consent-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.consent-label input {
  accent-color: #e77b9a;
  width: 17px;
  height: 17px;
}

.consent-box small {
  display: block;
  margin: 10px 0 0 27px;
  color: #987f87;
}

.permission {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 16px;
  margin-top: 18px;
  border-radius: 12px;
  background: #fff4f7;
  color: #795765;
  font-size: 14px;
}

.geo-actions {
  margin-top: 20px;
}

.geo-button,
.save-button {
  width: 100%;
  padding: 15px;
  border: none;
  border-radius: 12px;
  background: #e77b9a;
  color: white;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.2s;
}

.geo-button:hover:not(:disabled),
.save-button:hover:not(:disabled) {
  background: #d85d82;
}

.geo-button:disabled,
.save-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.coordinates,
.manual-location {
  margin-top: 28px;
  padding-top: 20px;
  border-top: 1px solid #f2e3e8;
}

.coordinates h2,
.manual-location h2 {
  margin-bottom: 16px;
  color: #b85570;
  font-size: 18px;
}

.result-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid #f7edf0;
  font-size: 14px;
}

.result-row span {
  color: #927d85;
}

.result-row strong {
  color: #44343a;
}

.maps-link {
  display: block;
  margin-top: 18px;
  padding: 14px;
  border-radius: 12px;
  background: #fff0f3;
  color: #b85570;
  text-align: center;
  text-decoration: none;
  font-weight: 700;
}

.manual-location input {
  width: 100%;
  padding: 14px;
  border: 1px solid #f0d5de;
  border-radius: 10px;
  outline: none;
  box-sizing: border-box;
  font-size: 14px;
}

.manual-location input:focus {
  border-color: #e77b9a;
}

.manual-location p {
  color: #987f87;
  font-size: 13px;
}

.geo-error,
.geo-success {
  margin-top: 18px;
  padding: 14px;
  border-radius: 10px;
  font-size: 14px;
}

.geo-error {
  background: #fff0f0;
  color: #bd3c50;
}

.geo-success {
  background: #eaf8f0;
  color: #287a52;
}

.save-button {
  margin-top: 22px;
}

.geo-info {
  margin-top: 24px;
  color: #a18c94;
  font-size: 12px;
  line-height: 1.6;
  text-align: center;
}

@media (max-width: 500px) {
  .geo-page {
    padding: 16px 10px;
  }

  .geo-card {
    padding: 22px 16px;
  }

  .geo-header h1 {
    font-size: 22px;
  }

  .result-row {
    flex-direction: column;
    gap: 5px;
  }
}
</style>
