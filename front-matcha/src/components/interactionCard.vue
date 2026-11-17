
<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  from_username?: string
  to_username?: string
  user_id: string
  typeOfInter: string
  created_at: string | Date
}>()

const emit = defineEmits<{
  clickOnProfile: [user_id: string]
}>()

const INTERACTION_LABEL: Record<
'from' | 'to',
Record<string, string>
> = {
  from: {
    Liked: 'liked you',
    Unliked: 'unliked you',
    Viewed: 'viewed your profile',
    Blocked: 'blocked you',
  },
  to: {
    Liked: 'You liked',
    Unliked: 'You unliked',
    Viewed: 'You viewed the profile of',
    Blocked: 'You blocked',
  },
}

const hasTarget = computed(() => props.to_username !== undefined)

const interactionLabel = computed(() => {
  const direction = hasTarget.value ? 'to' : 'from'
  
  return (
  INTERACTION_LABEL[direction][props.typeOfInter] ??
  props.typeOfInter
  )
})

const formattedDate = computed(() => {
  const date = new Date(props.created_at)
  
  if (Number.isNaN(date.getTime())) {
    return String(props.created_at)
  }
  
  return new Intl.DateTimeFormat('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
})

const datetimeValue = computed(() => {
  const date = new Date(props.created_at)
  
  return Number.isNaN(date.getTime())
  ? undefined
  : date.toISOString()
})

const typeClass = computed(() => {
  switch (props.typeOfInter) {
    case 'Liked':
    return 'interaction-card__type--liked'
    case 'Viewed':
    return 'interaction-card__type--viewed'
    case 'Blocked':
    return 'interaction-card__type--blocked'
    default:
    return 'interaction-card__type--default'
  }
})
</script>

<template>
  
  <article
  class="interaction-card"
  :class="{ 'interaction-card--with-target': hasTarget }"
  >
  <div class="interaction-card__icon" :class="typeClass">
    <span v-if="typeOfInter === 'Liked'">♥</span>
    <span v-else-if="typeOfInter === 'Viewed'">◉</span>
    <span v-else-if="typeOfInter === 'Blocked'">⊘</span>
    <span v-else>•</span>
  </div>
  
  <div class="interaction-card__content">
    <p class="interaction-card__description">
      <strong class="interaction-card__username" :title="from_username"
      @click="emit('clickOnProfile', user_id)">
        {{ from_username }}
      </strong>
      
      <span class="interaction-card__label">
        {{ interactionLabel }}
      </span>
      
      <strong
      v-if="hasTarget"
      class="interaction-card__username"
      :title="to_username"
      @click="emit('clickOnProfile', user_id)"
      >
      {{ to_username }}
    </strong>
  </p>
</div>

<div class="interaction-card__meta">
  <time
  v-if="datetimeValue"
  class="interaction-card__date"
  :datetime="datetimeValue"
  >
  {{ formattedDate }}
</time>
<span v-else class="interaction-card__date">
  {{ formattedDate }}
</span>

<span class="interaction-card__badge" :class="typeClass">
  {{ typeOfInter }}
</span>
</div>
</article>
</template>

<style scoped>

.interaction-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  margin-bottom: 16px;
  background: #ffffff;
  border: 1px solid #f1e5e5;
  border-radius: 24px;
  box-shadow: 0 5px 18px rgba(60, 30, 40, 0.05);
  transition: all 0.2s ease;
}

.interaction-card:hover {
  border-color: #f3cbd5;
  box-shadow: 0 10px 26px rgba(60, 30, 40, 0.08);
  transform: translateY(-2px);
}

.interaction-card__icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 16px;
  font-size: 21px;
}

.interaction-card__content {
  flex: 1;
  min-width: 0;
}

.interaction-card__description {
  color: #a7768b;
  font-size: 15px;
  line-height: 1.7;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  margin: 0;
}

.interaction-card__username {
  color: #58404c;
  font-weight: 600;
}

.interaction-card__username:hover {
    cursor: url('../../public/cursor.cur'), auto;
}
.interaction-card__meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 16px;
  flex-shrink: 0;
  margin-left: auto;
}

.interaction-card__date {
  color: #99878e;
  font-size: 13px;
  white-space: nowrap;
}

.interaction-card__badge {
  flex-shrink: 0;
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

/* Couleurs Matcha */

.interaction-card__type--liked {
  color: #ed6284;
  background-color: #fff0f3;
}

.interaction-card__type--viewed {
  color: #b85570;
  background-color: #fff1f4;
}

.interaction-card__type--blocked {
  color: #8e737b;
  background-color: #f8f1f3;
}

.interaction-card__type--default {
  color: #8b777d;
  background-color: #f5eff1;
}

@media (max-width: 600px) {
  .interaction-card {
    flex-wrap: wrap;
    gap: 12px;
    padding: 18px;
    margin-bottom: 12px;
  }

  .interaction-card__content {
    flex: 1;
    min-width: 0;
  }

  .interaction-card__meta {
    width: 100%;
    justify-content: flex-end;
    gap: 12px;
  }
}

</style>