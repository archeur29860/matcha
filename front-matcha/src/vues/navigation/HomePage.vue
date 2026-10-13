<script setup lang="ts">
import ListProfileCard from '@/components/listProfileCard.vue';
import SearchBarWithOption from '@/components/searchBarWithOption.vue';
import type { SearchOption } from '@/components/searchBarWithOption.vue';
import type { ProfileCard as ProfileCardType } from '@/types/profile';
import router from '@/router'
import { onMounted, ref, computed } from 'vue';
import { get_userProfile_list } from '@/services/api_userProfile'
import { useUserStore } from '@/stores/user';
import { useUserProfileStore } from '@/stores/userProfile';

const profiles = ref<ProfileCardType[]>([])

const userStore = useUserStore()
const userProfileStore = useUserProfileStore()

const hasMore = ref(true)
const next_cursor = ref("")
const loading = ref(true)

onMounted( async () => {
  const result = await get_userProfile_list(userStore.id)
  console.log("result:", result)
  profiles.value = result.data.profiles
  hasMore.value = result.data.has_more
  next_cursor.value = result.data.next_cursor
  loading.value = false
})

const searchOptions = computed<SearchOption[]>(() =>
  profiles.value.map((profile) => ({
    id: profile.user_id,
    label: profile.username,
    image: profile.image,
  }))
)


function handleProfileSelected(option: {
  id: string
  label: string
  subtitle?: string
  image?: string
}) {
  console.log('Profil sélectionné :', option.id)

  // Par exemple :
  userProfileStore.id = option.id
  router.push(`/profile/${option.id}/`)
}


function handleLike(user_id: string) {
  console.log('Liked', user_id)
}


function handleClickOnProfile(user_id: string) {
  console.log('Click on profile', user_id)
  router.push(`/profile/${user_id}/`)
  
}


async function loadMoreProfiles() {
  // Évite les appels simultanés ou inutiles.
  if (loading.value || !hasMore.value) return

  loading.value = true

  try {
    const result = await get_userProfile_list(
      userStore.id,
      20,
      next_cursor.value
    )
    console.log(result)

    if (!result.success) return

    // Adapte ce chemin au format exact de ta réponse API.
    const newProfiles = result.data.profiles

    // Ajoute les profils sans remplacer ceux déjà affichés.
    profiles.value.push(...newProfiles)

    next_cursor.value = result.data.next_cursor
    hasMore.value = result.data.has_more
  } catch (error) {
    console.error('Erreur lors du chargement des profils :', error)
  } finally {
    loading.value = false
  }

  console.log("profiles", profiles)
}

</script>


<template>
  <div class="profile-page">
    <div class="title-container"><h1 class="title">Connectez vous !</h1></div>
    <!-- Barre de recherche fixe -->
    <header class="search-header">
      <div class="search-container">
        <SearchBarWithOption
          :options="searchOptions"
          placeholder="Rechercher un utilisateur..."
          @select="handleProfileSelected"
        />
      </div>
    </header>

    <!-- Liste des profils -->
    <main class="profile-content">
      <ListProfileCard
        :profiles="profiles"
        :has-more="hasMore"
        :loading="loading"
        @load-more="loadMoreProfiles"
        @like="handleLike"
        @click-on-profile="handleClickOnProfile"
      />
    </main>
  </div>
</template>



<style scoped>

/* ============================
   TITRE
   ============================ */

.title-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.title {
  margin: 0;
  text-align: center;
  color: #e86f8d;
}

/* ============================
   PARENT
   ============================ */

.profile-page {
  position: relative;
  width: 100%;
  min-height: 100vh;
  box-sizing: border-box;
  isolation: isolate;

  --search-max-width: 680px;
  --search-padding-x: 16px;
}

/* ============================
   BARRE + DÉGRADÉ
   ============================ */

.search-header {
  position: sticky;
  top: 0;
  z-index: 1000;

  width: 100%;
  margin: 0;
  padding: 16px var(--search-padding-x) 48px;
  box-sizing: border-box;

  display: flex;
  justify-content: center;
  align-items: flex-start;

  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 1) 0%,
    rgba(255, 255, 255, 0.96) 30%,
    rgba(255, 255, 255, 0.75) 55%,
    rgba(255, 255, 255, 0.35) 78%,
    rgba(255, 255, 255, 0) 100%
  );

  pointer-events: none;
}

/* ============================
   CONTENEUR DE RECHERCHE
   ============================ */

.search-container {
  width: 100%;
  max-width: var(--search-max-width);
  min-width: 0;
  margin: 0 auto;

  display: flex;
  justify-content: center;

  pointer-events: auto;
}

/* Le composant occupe la largeur disponible */
.search-container > * {
  width: 100%;
  min-width: 0;
}

/* ============================
   LISTE DES PROFILS
   ============================ */

.profile-content {
  position: relative;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

/* ============================
   TABLETTES
   ============================ */

@media (max-width: 768px) {
  .profile-page {
    --search-padding-x: 16px;
  }

  .search-header {
    padding-top: 14px;
    padding-bottom: 40px;
  }
}

/* ============================
   MOBILES
   ============================ */

@media (max-width: 480px) {
  .profile-page {
    --search-padding-x: 12px;
  }

  .search-header {
    padding-top: 10px;
    padding-bottom: 32px;
  }
}

@media (max-width: 360px) {
  .profile-page {
    --search-padding-x: 8px;
  }
}

</style>


