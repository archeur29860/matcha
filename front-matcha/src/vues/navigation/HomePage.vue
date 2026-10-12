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

onMounted( async () => {
  const result = await get_userProfile_list(userStore.id)
  console.log("result:", result)
  profiles.value = result.data.profiles
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
</script>

<template>
    <SearchBarWithOption
    :options="searchOptions"
    placeholder="Rechercher un utilisateur..."
    @select="handleProfileSelected"
    />

    <ListProfileCard :profiles="profiles"
    @like="handleLike"
    @clickOnProfile="handleClickOnProfile"
    />
</template>
