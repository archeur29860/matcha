```vue
<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import type { ProfileCard as ProfileCardType } from '@/types/profile'
import ProfileCard from '@/components/profileCard.vue'

const props = defineProps<{
  profiles: ProfileCardType[]
  hasMore: boolean
  loading: boolean
}>()

const emit = defineEmits<{
  like: [user_id: string]
  clickOnProfile: [user_id: string]
  loadMore: []
}>()

const loadMoreTrigger = ref<HTMLElement | null>(null)

let observer: IntersectionObserver | null = null
let initialLoadFinished = false
let requestInProgress = false

function handleLike(user_id: string) {
  emit('like', user_id)
}

function handleClickOnProfile(user_id: string) {
  emit('clickOnProfile', user_id)
}

function observeTrigger() {
  observer?.disconnect()

  if (!loadMoreTrigger.value) return

  observer = new IntersectionObserver(
    ([entry]) => {
      if (!entry?.isIntersecting) return
      if (!initialLoadFinished) return
      if (props.loading || !props.hasMore) return
      if (requestInProgress) return

      requestInProgress = true
      emit('loadMore')
    },
    {
      root: null,
      rootMargin: '300px',
      threshold: 0
    }
  )

  observer.observe(loadMoreTrigger.value)
}

// Détecte la fin du chargement initial et des chargements suivants.
watch(
  () => props.loading,
  async (loading) => {
    if (loading) return

    initialLoadFinished = true

    // Attend la mise à jour du DOM avant de réobserver.
    await nextTick()

    requestInProgress = false
    observeTrigger()
  },
  { immediate: true }
)

onMounted(() => {
  observeTrigger()
})

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
})
</script>

<template>
  <div class="profiles-container">
    <div class="profiles">
      <ProfileCard
        v-for="profile in profiles"
        :key="profile.user_id"
        :profile="profile"
        @like="handleLike"
        @clickOnProfile="handleClickOnProfile"
      />
    </div>

    <!-- Déclencheur du défilement infini -->
    <div
      ref="loadMoreTrigger"
      class="load-more-trigger"
      aria-hidden="true"
    ></div>

    <div v-if="loading" class="loading">
      <span class="loading__spinner"></span>
      <span>Découverte de nouveaux profils...</span>
    </div>

    <p
      v-else-if="!hasMore && profiles.length > 0"
      class="end-message"
    >
      Vous avez découvert tous les profils disponibles 💗
    </p>

    <p
      v-else-if="!loading && profiles.length === 0"
      class="end-message"
    >
      Aucun profil à afficher pour le moment.
    </p>
  </div>
</template>

<style scoped>
.profiles-container {
  width: 100%;
  min-width: 0;
}

.profiles {
  display: grid;
  grid-template-columns: repeat(
    auto-fit,
    minmax(min(280px, 100%), 380px)
  );
  justify-content: center;
  gap: 24px;
}

.load-more-trigger {
  width: 100%;
  height: 1px;
  pointer-events: none;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 24px 12px;
  color: #a59a9f;
  font-size: 13px;
}

.loading__spinner {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  border: 2px solid #ffe1e7;
  border-top-color: #e86f8d;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

.end-message {
  margin: 12px 0;
  padding: 20px 12px;
  color: #a59a9f;
  font-size: 13px;
  text-align: center;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Tablette */
@media (max-width: 900px) {
  .profiles {
    gap: 20px;
  }
}

/* Mobile */
@media (max-width: 600px) {
  .profiles {
    grid-template-columns: minmax(0, 1fr);
    gap: 18px;
  }

  .loading {
    padding: 20px 8px;
    font-size: 12px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .loading__spinner {
    animation: none;
  }
}
</style>
```