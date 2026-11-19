
<script setup lang="ts">

import { ref } from 'vue'
import { upsert_situgeo } from '@/services/api_situgeo'
import { useUserStore } from '@/stores/user'
import Notification from '@/components/notification.vue'

const notificationRef = ref<InstanceType<typeof Notification> | null>(null)
const userStore = useUserStore()

// Localisation
const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)
const city = ref('')
const gpsConsent = ref(false)

// États
const loading = ref(false)
const saving = ref(false)
const permission = ref('Non demandée')

// Récapitulatif de la réponse API
const savedLocation = ref<Record<string, any> | null>(null)
const savedLocationSource = ref('')

// Notification des erreurs locales
function notifyError(message: string) {
    notificationRef.value?.make_notification({
        success: false,
        status: 400,
        error: {
            code: 'VALIDATION_ERROR',
            message
        }
    })
}

// Récupération GPS
function getCurrentLocation() {
    if (!gpsConsent.value) {
        notifyError("Tu dois accepter l'utilisation du GPS.")
        return
    }

    if (!navigator.geolocation) {
        notifyError("La géolocalisation n'est pas supportée.")
        return
    }

    loading.value = true
    permission.value = 'En attente...'

    navigator.geolocation.getCurrentPosition(
        (position) => {
            latitude.value = position.coords.latitude
            longitude.value = position.coords.longitude

            permission.value = 'Autorisée'
            loading.value = false

            notificationRef.value?.make_notification({
                success: true
            })
        },
        (err) => {
            loading.value = false

            let message = 'Une erreur GPS est survenue.'

            switch (err.code) {
                case err.PERMISSION_DENIED:
                    permission.value = 'Refusée'
                    message = "Tu as refusé l'accès à ta position."
                    break

                case err.POSITION_UNAVAILABLE:
                    message = 'Position GPS indisponible.'
                    break

                case err.TIMEOUT:
                    message = 'Le délai de recherche GPS est dépassé.'
                    break
            }

            notifyError(message)
        },
        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }
    )
}

// Gestion du consentement
function handleConsentChange() {
    if (!gpsConsent.value) {
        latitude.value = null
        longitude.value = null
        permission.value = 'Non demandée'
    }
}

// Enregistrement de la localisation
async function saveLocation() {
    savedLocation.value = null
    savedLocationSource.value = ''

    if (!userStore.id) {
        notifyError('Identifiant utilisateur manquant.')
        return
    }

    const hasGPS = latitude.value !== null && longitude.value !== null
    const hasCity = city.value.trim().length > 0

    if (!hasGPS && !hasCity) {
        notifyError('Récupère ta position GPS ou renseigne une ville.')
        return
    }

    if (hasGPS && !gpsConsent.value) {
        notifyError('Le consentement GPS est nécessaire.')
        return
    }

    saving.value = true

    const response = await upsert_situgeo(
        userStore.id,
        hasGPS,
        hasGPS ? latitude.value! : undefined,
        hasGPS ? longitude.value! : undefined,
        hasGPS ? undefined : city.value.trim()
    )

    saving.value = false

    if (response == null) {
        notifyError("Aucune réponse reçue lors de l'enregistrement.")
        return
    }

    // Notification du résultat API
    notificationRef.value?.make_notification(response)

    // Affichage du récapitulatif uniquement en cas de succès
    if (response.success) {
        savedLocation.value = response.data ?? response
        savedLocationSource.value = hasGPS ? 'GPS' : 'Ville renseignée'
    }
}

// Affichage des valeurs du récapitulatif
function formatValue(value: unknown): string {
    if (value === null || value === undefined) {
        return 'Non renseigné'
    }

    if (typeof value === 'object') {
        return JSON.stringify(value, null, 2)
    }

    if (typeof value === 'boolean') {
        return value ? 'Oui' : 'Non'
    }

    return String(value)
}

// Libellés plus lisibles pour les champs courants
function formatLabel(key: string): string {
    const labels: Record<string, string> = {
        id: 'Identifiant',
        user_id: 'Utilisateur',
        city: 'Ville',
        latitude: 'Latitude',
        longitude: 'Longitude',
        source: 'Source',
        created_at: 'Date de création',
        updated_at: 'Dernière mise à jour',
        message: 'Message'
    }

    return labels[key] ?? key.replaceAll('_', ' ')
}

</script>

<template>
    <main class="geo-page">
        <section class="geo-card">

            <header class="geo-header">
                <span class="geo-icon">📍</span>
                <h1>Ma localisation</h1>
                <p>Indique ta position pour profiter pleinement de Matcha.</p>
            </header>

            <!-- Consentement GPS -->
            <div class="consent-box">
                <label class="consent-label">
                    <input v-model="gpsConsent" type="checkbox" @change="handleConsentChange" />
                    <span>J'accepte de partager ma position GPS.</span>
                </label>

                <small>
                    Tu peux également renseigner ta ville manuellement.
                </small>
            </div>

            <!-- Permission GPS -->
            <div class="permission">
                <span>Autorisation GPS</span>
                <strong>{{ permission }}</strong>
            </div>

            <!-- Récupération GPS -->
            <div class="geo-actions">
                <button class="geo-button" :disabled="loading || saving || !gpsConsent" @click="getCurrentLocation">
                    {{ loading ? 'Recherche...' : 'Obtenir ma position GPS' }}
                </button>
            </div>

            <!-- Coordonnées -->
            <div v-if="latitude !== null && longitude !== null" class="coordinates">
                <h2>Position récupérée</h2>

                <div class="result-row">
                    <span>Latitude</span>
                    <strong>{{ latitude.toFixed(6) }}</strong>
                </div>

                <div class="result-row">
                    <span>Longitude</span>
                    <strong>{{ longitude.toFixed(6) }}</strong>
                </div>

                <a :href="`https://www.google.com/maps?q=${latitude},${longitude}`" target="_blank"
                    rel="noopener noreferrer" class="maps-link">
                    Voir ma position sur Google Maps ↗
                </a>
            </div>

            <!-- Ville manuelle -->
            <div class="manual-location">
                <h2>Ou renseigner une ville</h2>

                <input v-model="city" type="text" placeholder="Ex : Paris, Lyon, Marseille..." :disabled="saving" />

                <p>
                    Cette option permet d'enregistrer ta localisation sans utiliser
                    le GPS.
                </p>
            </div>

            <!-- Enregistrement -->
            <button class="save-button" :disabled="saving || loading" @click="saveLocation">
                {{ saving ? 'Enregistrement...' : 'Enregistrer ma localisation' }}
            </button>

            <!-- Récapitulatif de la réponse API -->
            <div v-if="savedLocation" class="coordinates">
                <h2>✓ Localisation enregistrée</h2>

                <p>
                    Ta localisation a bien été enregistrée.
                </p>

                <div class="result-row">
                    <span>Mode d'enregistrement</span>
                    <strong>{{ savedLocationSource }}</strong>
                </div>

                <div
                    v-for="(value, key) in savedLocation"
                    :key="String(key)"
                    class="result-row"
                >
                    <span>{{ formatLabel(String(key)) }}</span>
                    <strong>{{ formatValue(value) }}</strong>
                </div>
            </div>

            <p class="geo-info">
                Tes informations de localisation sont utilisées conformément
                à ton consentement.
            </p>

        </section>

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
