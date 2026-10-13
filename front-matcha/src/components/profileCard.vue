<script setup lang="ts">
import { computed } from 'vue'
import type { ProfileCard } from '@/types/profile'

const props = defineProps<{
  profile: ProfileCard
}>()

const emit = defineEmits<{
  like: [user_id: string]
  clickOnProfile: [user_id: string]
}>()

const popularityLabel = computed(() => {
  if (props.profile.popularity >= 90) return 'Ultra populaire'
  if (props.profile.popularity >= 70) return 'Très populaire'
  if (props.profile.popularity >= 40) return 'Populaire'

  return 'Nouveau'
})

const popularityClass = computed(() => {
  if (props.profile.popularity >= 90) return 'ultra'
  if (props.profile.popularity >= 70) return 'high'
  if (props.profile.popularity >= 40) return 'medium'

  return 'low'
})
</script>

<template>
  <article class="profile-card">
    <!-- Image -->
    <div class="profile-card__image-wrapper">
      <img
        :src="'http://localhost:5000/api/pictures/' + profile.image"
        :alt="`Photo de ${profile.username}`"
        class="profile-card__image"
      />

      <!-- Badge online -->
      <div
        v-if="profile.online"
        class="profile-card__online"
      >
        <span class="profile-card__online-dot"></span>
        En ligne
      </div>

      <!-- Popularité -->
      <div
        class="profile-card__popularity"
        :class="`profile-card__popularity--${popularityClass}`"
      >
        <span class="profile-card__popularity-icon">
          ♥
        </span>

        <div class="profile-card__popularity-info">
          <strong>
            {{ popularityLabel }}
          </strong>

          <div class="profile-card__popularity-bar">
            <span
              :style="{
                width: `${profile.popularity}%`
              }"
            ></span>
          </div>
        </div>

        <span class="profile-card__popularity-score">
          {{ profile.popularity }}
        </span>
      </div>
    </div>

    <!-- Contenu -->
    <div class="profile-card__content">
      <!-- Header -->
      <header class="profile-card__header">
        <div>
          <h2 class="profile-card__username" @click="emit('clickOnProfile', profile.user_id)">
            {{ profile.username }}, {{ profile.age }}
          </h2>

          <p class="profile-card__location">
            <span>📍</span>
            {{ profile.location }}
          </p>
        </div>
      </header>

      <!-- Tags -->
      <div class="profile-card__tags">
        <span
          v-for="tag in profile.tags"
          :key="tag.id"
          class="profile-card__tag"
        >
          {{ tag.label }}
        </span>
      </div>

      <!-- Bio -->
      <p class="profile-card__bio">
        {{ profile.bio }}
      </p>

      <!-- Actions -->
      <div class="profile-card__actions">
        <button
          type="button"
          class="profile-card__action profile-card__action--like"
          aria-label="Liker ce profil"
          @click="emit('like', profile.user_id)"
        >
          <span>♥</span>
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.profile-card {
  width: 100%;
  max-width: 380px;
  overflow: hidden;
  background: #ffffff;
  border: 1px solid #f1e5e5;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(60, 30, 40, 0.08);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.profile-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(60, 30, 40, 0.12);
}

/* =========================================
   IMAGE
========================================= */

.profile-card__image-wrapper {
  position: relative;
  width: 100%;
  height: 380px;
  overflow: hidden;
  background: #f8eeee;
}

.profile-card__image {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

/* =========================================
   ONLINE
========================================= */

.profile-card__online {
  position: absolute;
  top: 16px;
  left: 16px;

  display: flex;
  align-items: center;
  gap: 6px;

  padding: 7px 10px;

  color: #ffffff;
  font-size: 12px;
  font-weight: 600;

  background: rgba(35, 35, 35, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 999px;

  backdrop-filter: blur(8px);
}

.profile-card__online-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #48c774;
}

/* =========================================
   POPULARITÉ
========================================= */

.profile-card__popularity {
  position: absolute;
  top: 16px;
  right: 16px;

  display: flex;
  align-items: center;
  gap: 8px;

  min-width: 155px;
  padding: 8px 10px;

  background: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 14px;

  box-shadow: 0 5px 15px rgba(30, 15, 20, 0.1);

  backdrop-filter: blur(10px);
}

.profile-card__popularity-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 28px;
  height: 28px;

  color: #ed6284;
  font-size: 16px;

  background: #fff0f3;
  border-radius: 9px;
}

.profile-card__popularity-info {
  flex: 1;
  min-width: 0;
}

.profile-card__popularity-info strong {
  display: block;
  margin-bottom: 5px;

  color: #3c2930;
  font-size: 10px;
  font-weight: 700;
  white-space: nowrap;
}

.profile-card__popularity-bar {
  width: 100%;
  height: 4px;

  overflow: hidden;

  background: #f0e5e8;
  border-radius: 999px;
}

.profile-card__popularity-bar span {
  display: block;
  height: 100%;

  border-radius: inherit;

  background: linear-gradient(
    90deg,
    #f6a2b5,
    #ed6284
  );

  transition: width 0.3s ease;
}

.profile-card__popularity-score {
  color: #ed6284;
  font-size: 12px;
  font-weight: 700;
}

/* =========================================
   POPULARITÉ - NIVEAUX
========================================= */

.profile-card__popularity--ultra
  .profile-card__popularity-icon {
  color: #d94b70;
  background: #ffe4eb;
}

.profile-card__popularity--high
  .profile-card__popularity-icon {
  color: #e46b86;
  background: #ffedf1;
}

.profile-card__popularity--medium
  .profile-card__popularity-icon {
  color: #d58a5d;
  background: #fff1e8;
}

.profile-card__popularity--low
  .profile-card__popularity-icon {
  color: #999999;
  background: #f1f1f1;
}

/* =========================================
   CONTENT
========================================= */

.profile-card__content {
  padding: 20px;
}

/* =========================================
   HEADER
========================================= */

.profile-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 14px;
}

.profile-card__username {
  margin: 0;

  color: #302329;
  font-size: 22px;
  font-weight: 700;
  line-height: 1.2;
}

.profile-card__username:hover {
    cursor: url('../../public/cursor.cur'), auto;
}


.profile-card__location {
  display: flex;
  align-items: center;
  gap: 4px;

  margin: 7px 0 0;

  color: #8b777d;
  font-size: 13px;
}

/* =========================================
   TAGS
========================================= */

.profile-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;

  margin-bottom: 16px;
}

.profile-card__tag {
  padding: 6px 10px;

  color: #b85570;
  font-size: 11px;
  font-weight: 600;

  background: #fff1f4;
  border-radius: 999px;
}

/* =========================================
   BIO
========================================= */

.profile-card__bio {
  margin: 0;

  color: #66565c;
  font-size: 14px;
  line-height: 1.6;
}

/* =========================================
   ACTIONS
========================================= */

.profile-card__actions {
  display: flex;
  justify-content: center;
  gap: 14px;

  margin-top: 22px;
}

.profile-card__action {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 52px;
  height: 52px;

  cursor: pointer;

  border: 0;
  border-radius: 50%;

  font-size: 21px;

  transition:
    transform 0.2s ease,
    background 0.2s ease,
    box-shadow 0.2s ease;
}

.profile-card__action:hover {
  transform: scale(1.08);
}

.profile-card__action:active {
  transform: scale(0.95);
}

.profile-card__action--dislike {
  color: #8e737b;
  background: #f8f1f3;
}

.profile-card__action--dislike:hover {
  background: #f1e5e8;
  box-shadow: 0 6px 16px rgba(80, 50, 60, 0.12);
}

.profile-card__action--like {
  color: #ffffff;
  background: linear-gradient(
    135deg,
    #f48ba4,
    #e95f80
  );
  box-shadow: 0 7px 18px rgba(233, 95, 128, 0.25);
}

.profile-card__action--like:hover {
  box-shadow: 0 10px 24px rgba(233, 95, 128, 0.35);
}

/* =========================================
   RESPONSIVE
========================================= */

@media (max-width: 600px) {
  .profile-card {
    max-width: 100%;
    border-radius: 20px;
  }

  .profile-card__image-wrapper {
    height: 340px;
  }

  .profile-card__popularity {
    min-width: 145px;
    top: 12px;
    right: 12px;
  }

  .profile-card__online {
    top: 12px;
    left: 12px;
  }

  .profile-card__content {
    padding: 18px;
  }

  .profile-card__username {
    font-size: 20px;
  }
}
</style>