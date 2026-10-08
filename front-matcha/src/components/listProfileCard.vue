<script setup lang="ts">
import type { ProfileCard as ProfileCardType } from '@/types/profile'
import ProfileCard from '@/components/profileCard.vue'

const props = defineProps<{
  profiles: ProfileCardType[]
}>()

const emit = defineEmits<{
  like: [user_id: string]
  clickOnProfile: [user_id: string]
}>()

function handleLike(user_id: string) {
  console.log('Liked', user_id)
  emit('like', user_id)
}


function handleClickOnProfile(user_id: string) {
  console.log('Click on profile', user_id)
  emit('clickOnProfile', user_id)
}

</script>

<template>
      <div class="profiles">
        <ProfileCard
          v-for="profile in profiles"
          :key="profile.user_id"
          :profile="profile"
          @like="handleLike"
          @clickOnProfile="handleClickOnProfile"
        />
      </div>
</template>

<style scoped>
.layout {
  min-height: 100vh;
  width: 100%;
}

/* ================================
   CONTENT
================================ */

.discover {
  margin-left: 250px;
  min-width: 0;

  padding: 32px 24px;

  box-sizing: border-box;
}

/* ================================
   PROFILES
================================ */

.profiles {
  display: grid;

  grid-template-columns: repeat(
    auto-fit,
    minmax(280px, 380px)
  );

  justify-content: center;

  gap: 24px;
}

/* ================================
   TABLET
================================ */

@media (max-width: 900px) {
  .discover {
    margin-left: 76px;
    padding: 28px 20px;
  }
}

/* ================================
   MOBILE
================================ */

@media (max-width: 600px) {
  .discover {
    margin-left: 0;

    padding: 16px;
    padding-bottom: 90px;
  }

  .profiles {
    grid-template-columns: 1fr;
  }
}
</style>