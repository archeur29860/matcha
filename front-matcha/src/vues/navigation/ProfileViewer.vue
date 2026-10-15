```vue
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import ReportModal from '@/components/modal/reportModal.vue'
import Notification from '@/components/notification.vue'
import { useRoute } from 'vue-router'

import { useUserProfileStore } from '@/stores/userProfile'
import { get_userProfile } from '@/services/api_userProfile'

const userProfileStore = useUserProfileStore()

const notificationRef = ref<InstanceType<typeof Notification> | null>(null)
const liked = ref(false)
const showReportModal = ref(false)
const loading = ref(true)
const loadError = ref('')

type ReportReason = 'fake_account' | 'scam' | 'problematic'

const API_BASE_URL = 'http://localhost:5000/api'

const route = useRoute()

onMounted(async () => {
  try {
    const result = await get_userProfile(String(route.params.user_id))

    // console.log('Réponse API :', result)
    notificationRef.value?.make_notification(result)

    if (!result.success || !result.data) {
      loadError.value = 'Impossible de récupérer le profil.'
      return
    }

    const data = result.data

    userProfileStore.id = data.user_id
    userProfileStore.username = data.username
    userProfileStore.first_name = data.first_name
    userProfileStore.last_name = data.last_name
    userProfileStore.last_connection = data.last_connection ?? null

    // Si data.age est une date de naissance.
    userProfileStore.age = data.age
      ? new Date().getFullYear() - new Date(data.age).getFullYear()
      : 0

    userProfileStore.gender = data.gender ?? ''
    userProfileStore.gender_pref = data.gender_pref.split(',') ?? []
    userProfileStore.bio = data.bio ?? ''
    userProfileStore.picture_profile_index = data.picture_profile_index
    userProfileStore.popularity = data.popularity ?? 0
    userProfileStore.location = data.location ?? 'Ville non renseignée'
    userProfileStore.tags = data.tags ?? []
    userProfileStore.pictures = data.pictures ?? []

    // console.log('Photos récupérées :', userProfileStore.pictures)
  } catch (error) {
    console.error('Erreur de récupération du profil :', error)
    loadError.value = 'Une erreur est survenue lors du chargement du profil.'
  } finally {
    loading.value = false
  }
})

const mainPicture = computed(() => {
  const pictures = userProfileStore.pictures ?? []
	const mainpic = pictures.filter(
		picture => picture.id == userProfileStore.picture_profile_index
  )
  // console.log("mainpic", mainpic)
  if (mainpic[0]) {
    return mainpic[0].url
  }
  return null
})

const secondaryPictures = computed(() => {
  const pictures = userProfileStore.pictures ?? []

  return pictures.filter(
    picture => picture.id !== userProfileStore.picture_profile_index
  )
})

const formattedLastConnection = computed(() => {
  const value = userProfileStore.last_connection

  if (!value) return 'Inconnue'

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) return 'Inconnue'

  return new Intl.DateTimeFormat('fr-FR', {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(date)
})

function handleLike() {
  liked.value = true
  // Ajouter ici l'appel API pour liker le profil.
}

function handleUnlike() {
  liked.value = false
  // Ajouter ici l'appel API pour retirer le like.
}

function handleReport() {
  showReportModal.value = true
}

function handleReportSubmit(reason: ReportReason) {
  showReportModal.value = false
  // console.log('Utilisateur signalé :', userProfileStore.id)
  // console.log('Raison :', reason)
  // Ajouter ici l'appel API de signalement.
}

function handleBlocked() {
  // console.log('Utilisateur bloqué :', userProfileStore.id)
  // Ajouter ici l'appel API de blocage.
}
</script>

<template>
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

  <main class="profile-viewer">
    <div v-if="loading" class="profile-viewer__status">
      Chargement du profil…
    </div>

    <div v-else-if="loadError" class="profile-viewer__status profile-viewer__status--error">
      {{ loadError }}
    </div>

    <template v-else>
      <!-- Photos -->
      <section class="profile-viewer__photos">
        <div v-if="mainPicture" class="profile-viewer__main-photo">
          <img
            :src="'http://localhost:5000/api/pictures/' + mainPicture"
            :alt="`Photo de ${userProfileStore.first_name} ${userProfileStore.last_name}`"
          />
        </div>

        <div v-else class="profile-viewer__no-photo">
          <span>📷</span>
          <p>Aucune photo</p>
        </div>

        <div
          v-if="secondaryPictures.length > 0"
          class="profile-viewer__gallery"
        >
          <div
            v-for="picture in secondaryPictures"
            :key="picture.id"
            class="profile-viewer__gallery-item"
          >
            <img
              :src="'http://localhost:5000/api/pictures/' + picture.url"
              :alt="`Photo ${picture.id + 1} de ${userProfileStore.first_name} ${userProfileStore.last_name}`"
              loading="lazy"
            />
          </div>
        </div>
      </section>

      <!-- Informations du profil -->
      <section class="profile-viewer__info">
        <header class="profile-viewer__header">
          <div>
            <h1>
              {{ userProfileStore.first_name }}
              {{ userProfileStore.last_name }}
            </h1>

            <p class="profile-viewer__username">
              @{{ userProfileStore.username }}
            </p>
          </div>

          <span class="profile-viewer__age">
            {{ userProfileStore.age }} ans
          </span>
        </header>

        <!-- Localisation et dernière connexion -->
        <div class="profile-viewer__meta">
          <div class="profile-viewer__location">
            <span>📍</span>
            <span>{{ userProfileStore.location }}</span>
          </div>

          <div class="profile-viewer__last-connection">
            <span>🕒</span>
            <span>Dernière connexion : {{ formattedLastConnection }}</span>
          </div>
        </div>

        <!-- Genre, préférences et popularité -->
        <div class="profile-viewer__details">
          <article class="profile-viewer__detail">
            <h2>Genre</h2>
            <p>{{ userProfileStore.gender || 'Non renseigné' }}</p>
          </article>

          <article class="profile-viewer__detail">
            <h2>Recherche</h2>
            <p>
              {{
                userProfileStore.gender_pref?.length
                  ? userProfileStore.gender_pref.join(', ')
                  : 'Non renseigné'
              }}
            </p>
          </article>

          <article class="profile-viewer__detail">
            <h2>Popularité</h2>
            <p>{{ userProfileStore.popularity ?? 0 }}</p>
          </article>
        </div>

        <!-- Biographie -->
        <section class="profile-viewer__bio">
          <h2>À propos</h2>
          <p>
            {{ userProfileStore.bio || 'Aucune biographie renseignée.' }}
          </p>
        </section>

        <!-- Tags -->
        <section class="profile-viewer__tags">
          <h2>Centres d’intérêt</h2>

          <div
            v-if="userProfileStore.tags?.length"
            class="profile-viewer__tags-list"
          >
            <span
              v-for="tag in userProfileStore.tags"
              :key="tag.id"
              class="profile-viewer__tag"
            >
              {{ tag.label }}
            </span>
          </div>

          <p v-else class="profile-viewer__empty">
            Aucun centre d’intérêt renseigné.
          </p>
        </section>

        <!-- Actions -->
        <div class="profile-viewer__actions">
          <button
            v-if="!liked"
            type="button"
            class="profile-viewer__button profile-viewer__button--like"
            @click="handleLike"
          >
            <span>♥</span>
            Liker
          </button>

          <button
            v-else
            type="button"
            class="profile-viewer__button profile-viewer__button--unlike"
            @click="handleUnlike"
          >
            <span>♥</span>
            Retirer le like
          </button>

          <button
            type="button"
            class="profile-viewer__button profile-viewer__button--block"
            @click="handleBlocked"
          >
            <span>⚑</span>
            Bloquer
          </button>

          <button
            type="button"
            class="profile-viewer__button profile-viewer__button--report"
            @click="handleReport"
          >
            <span>⚑</span>
            Signaler
          </button>
        </div>
      </section>
    </template>

    <ReportModal
      :open="showReportModal"
      @close="showReportModal = false"
      @report="handleReportSubmit"
    />
  </main>
</template>

<style scoped>
.profile-viewer {
  width: 100%;
  min-height: 100%;
  background: #fff;
}

.profile-viewer__status {
  padding: 48px 24px;
  text-align: center;
  color: #8b777d;
}

.profile-viewer__status--error {
  color: #b42345;
}

/* Photos */

.profile-viewer__photos {
  width: 100%;
  max-width: 1100px;
  margin: 0 auto;
}

.profile-viewer__main-photo {
  width: 100%;
  height: min(70vh, 700px);
  min-height: 400px;
  overflow: hidden;
  background: #f8eeee;
}

.profile-viewer__main-photo img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.profile-viewer__no-photo {
  width: 100%;
  height: 500px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #f8eeee;
  color: #8b777d;
}

.profile-viewer__no-photo span {
  font-size: 42px;
}

.profile-viewer__no-photo p {
  margin: 0;
}

.profile-viewer__gallery {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 4px;
  margin-top: 4px;
}

.profile-viewer__gallery-item {
  height: 220px;
  overflow: hidden;
  background: #f8eeee;
}

.profile-viewer__gallery-item img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
  transition: transform 0.25s ease;
}

.profile-viewer__gallery-item:hover img {
  transform: scale(1.03);
}

/* Informations */

.profile-viewer__info {
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
  padding: 36px 24px 48px;
}

.profile-viewer__header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
}

.profile-viewer__header h1 {
  margin: 0;
  color: #302329;
  font-size: 34px;
  line-height: 1.15;
  font-weight: 700;
  overflow-wrap: anywhere;
}

.profile-viewer__username {
  margin: 8px 0 0;
  color: #b85570;
  font-size: 16px;
}

.profile-viewer__age {
  color: #8b777d;
  font-size: 20px;
  white-space: nowrap;
}

.profile-viewer__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 24px;
  margin-top: 18px;
}

.profile-viewer__location,
.profile-viewer__last-connection {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #8b777d;
  font-size: 14px;
  overflow-wrap: anywhere;
}

.profile-viewer__details {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 28px;
}

.profile-viewer__detail {
  min-width: 0;
  padding: 18px;
  border: 1px solid #f6d5de;
  border-radius: 14px;
  background: #fff8fa;
}

.profile-viewer__detail h2,
.profile-viewer__bio h2,
.profile-viewer__tags h2 {
  margin: 0 0 10px;
  color: #b85570;
  font-size: 16px;
  font-weight: 700;
}

.profile-viewer__detail p {
  margin: 0;
  color: #302329;
  overflow-wrap: anywhere;
}

/* Biographie */

.profile-viewer__bio {
  margin-top: 28px;
  padding: 22px;
  border-radius: 14px;
  background: #fdf5f7;
}

.profile-viewer__bio p {
  margin: 0;
  color: #55444a;
  line-height: 1.7;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

/* Centres d'intérêt */

.profile-viewer__tags {
  margin-top: 28px;
}

.profile-viewer__tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.profile-viewer__tag {
  padding: 8px 14px;
  border: 1px solid #f6d5de;
  border-radius: 999px;
  background: #fff0f3;
  color: #b85570;
  font-size: 14px;
  font-weight: 600;
}

.profile-viewer__empty {
  color: #8b777d;
  font-size: 14px;
}

/* Actions */

.profile-viewer__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.profile-viewer__button {
  min-height: 48px;
  padding: 0 24px;
  border: 0;
  border-radius: 14px;
  font: inherit;
  font-weight: 600;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.profile-viewer__button:hover {
  transform: translateY(-1px);
}

.profile-viewer__button:active {
  transform: translateY(0);
}

.profile-viewer__button--like {
  flex: 1;
  color: white;
  background: linear-gradient(135deg, #f6a2b5, #ed6284);
  box-shadow: 0 8px 20px rgba(237, 98, 132, 0.22);
}

.profile-viewer__button--like:hover {
  box-shadow: 0 10px 24px rgba(237, 98, 132, 0.3);
}

.profile-viewer__button--unlike {
  flex: 1;
  color: #b85570;
  background: #fff0f3;
  border: 1px solid #f6d5de;
}

.profile-viewer__button--report,
.profile-viewer__button--block {
  color: #8b777d;
  background: #f8f1f3;
}

.profile-viewer__button--report:hover,
.profile-viewer__button--block:hover {
  color: #b85570;
  background: #fff0f3;
}

.profile-viewer__button span {
  margin-right: 6px;
}

/* Tablette */

@media (max-width: 800px) {
  .profile-viewer__main-photo {
    height: 60vh;
    min-height: 350px;
  }

  .profile-viewer__gallery-item {
    height: 180px;
  }

  .profile-viewer__info {
    padding: 28px 20px 40px;
  }

  .profile-viewer__details {
    gap: 10px;
  }

  .profile-viewer__detail {
    padding: 14px;
  }

  .profile-viewer__bio {
    padding: 18px;
  }
}

/* Mobile */

@media (max-width: 600px) {
  .profile-viewer__main-photo {
    height: 65vh;
    min-height: 320px;
    max-height: 550px;
  }

  .profile-viewer__gallery {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .profile-viewer__gallery-item {
    height: 180px;
  }

  .profile-viewer__info {
    padding: 24px 16px 32px;
  }

  .profile-viewer__header {
    align-items: flex-start;
  }

  .profile-viewer__header h1 {
    font-size: 27px;
  }

  .profile-viewer__age {
    font-size: 17px;
  }

  .profile-viewer__meta {
    flex-direction: column;
    gap: 10px;
  }

  .profile-viewer__details {
    grid-template-columns: 1fr;
    gap: 12px;
    margin-top: 22px;
  }

  .profile-viewer__detail {
    padding: 16px;
  }

  .profile-viewer__bio,
  .profile-viewer__tags {
    margin-top: 22px;
  }

  .profile-viewer__bio {
    padding: 16px;
  }

  .profile-viewer__actions {
    flex-direction: column;
    margin-top: 26px;
  }

  .profile-viewer__button {
    width: 100%;
  }
}

/* Petit mobile */

@media (max-width: 400px) {
  .profile-viewer__main-photo {
    height: 60vh;
    min-height: 280px;
  }

  .profile-viewer__gallery-item {
    height: 140px;
  }

  .profile-viewer__header h1 {
    font-size: 24px;
  }
}
</style>
```