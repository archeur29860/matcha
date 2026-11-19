
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
    Reported: 'reported you',
  },
  to: {
    Liked: 'You liked',
    Unliked: 'You unliked',
    Viewed: 'You viewed the profile of',
    Blocked: 'You blocked',
    Reported: 'You reported',
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
    case 'Unliked':
      return 'interaction-card__type--unliked'
    case 'Viewed':
      return 'interaction-card__type--viewed'
    case 'Blocked':
      return 'interaction-card__type--blocked'
    case 'Reported':
      return 'interaction-card__type--reported'
    default:
      return 'interaction-card__type--default'
  }
})

const interactionIcon = computed(() => {
  switch (props.typeOfInter) {
    case 'Liked':
      return '♥'
    case 'Unliked':
      return '♡'
    case 'Viewed':
      return '◉'
    case 'Blocked':
      return '⊘'
    case 'Reported':
      return '⚑'
    default:
      return '•'
  }
})
</script>

<template>
  <article
    class="interaction-card"
    :class="{ 'interaction-card--with-target': hasTarget }"
  >
    <div class="interaction-card__icon" :class="typeClass">
      <span>{{ interactionIcon }}</span>
    </div>

    <div class="interaction-card__content">
      <p class="interaction-card__description">

        <strong
          class="interaction-card__username"
          :title="from_username"
          @click="emit('clickOnProfile', user_id)"
        >
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

/* =========================
   CARTE
========================= */

.interaction-card {
  display: flex;
  align-items: center;
  gap: 16px;

  width: 100%;
  min-width: 0;
  box-sizing: border-box;

  padding: 20px;

  background: #ffffff;
  border: 1px solid #f1e5e5;
  border-radius: 20px;

  box-shadow: 0 5px 18px rgba(60, 30, 40, 0.05);

  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.interaction-card:hover {
  border-color: #f3cbd5;
  box-shadow: 0 10px 26px rgba(60, 30, 40, 0.08);
  transform: translateY(-2px);
}

/* =========================
   ICÔNE
========================= */

.interaction-card__icon {
  flex-shrink: 0;

  width: 46px;
  height: 46px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 15px;
  font-size: 21px;
}

/* =========================
   CONTENU
========================= */

.interaction-card__content {
  flex: 1;
  min-width: 0;
}

.interaction-card__description {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 5px;

  margin: 0;

  color: #a7768b;
  font-size: 14px;
  line-height: 1.6;
}

/* =========================
   USERNAME
========================= */

.interaction-card__username {
  color: #58404c;
  font-weight: 600;
  cursor: pointer;
  overflow-wrap: anywhere;
  transition: color 0.2s ease;
}

.interaction-card__username:hover {
  color: #ed6284;
}

/* =========================
   MÉTADONNÉES
========================= */

.interaction-card__meta {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;

  flex-shrink: 0;
  margin-left: auto;
}

.interaction-card__date {
  color: #99878e;
  font-size: 12px;
  white-space: nowrap;
}

.interaction-card__badge {
  flex-shrink: 0;

  padding: 7px 12px;
  border-radius: 999px;

  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

/* =========================
   COULEURS MATCHA
========================= */

.interaction-card__type--liked {
  color: #ed6284;
  background-color: #fff0f3;
}

.interaction-card__type--unliked {
  color: #a7768b;
  background-color: #f8f1f4;
}

.interaction-card__type--viewed {
  color: #b85570;
  background-color: #fff1f4;
}

.interaction-card__type--blocked {
  color: #8e737b;
  background-color: #f8f1f3;
}

.interaction-card__type--reported {
  color: #a05b45;
  background-color: #fff1e9;
}

.interaction-card__type--default {
  color: #8b777d;
  background-color: #f5eff1;
}

/* =========================
   TABLETTES
========================= */

@media (max-width: 900px) {
  .interaction-card {
    padding: 16px;
    gap: 12px;
  }

  .interaction-card__icon {
    width: 42px;
    height: 42px;
  }

  .interaction-card__meta {
    gap: 8px;
  }
}

/* =========================
   MOBILES
========================= */

@media (max-width: 600px) {
  .interaction-card {
    display: grid;
    grid-template-columns: 42px minmax(0, 1fr);
    gap: 10px;

    padding: 14px;
    border-radius: 16px;
  }

  .interaction-card__icon {
    width: 42px;
    height: 42px;
    grid-row: 1;
  }

  .interaction-card__content {
    grid-column: 2;
    grid-row: 1;
  }

  .interaction-card__description {
    font-size: 13px;
    gap: 4px;
  }

  .interaction-card__meta {
    grid-column: 1 / -1;
    grid-row: 2;

    width: 100%;
    justify-content: space-between;

    margin-left: 0;
    padding-top: 8px;

    border-top: 1px solid #f7edef;
  }

  .interaction-card__date {
    font-size: 11px;
  }

  .interaction-card__badge {
    padding: 6px 10px;
    font-size: 10px;
  }
}

/* =========================
   PETITS MOBILES
========================= */

@media (max-width: 360px) {
  .interaction-card {
    padding: 11px;
    gap: 8px;
  }

  .interaction-card__icon {
    width: 36px;
    height: 36px;
    border-radius: 12px;
    font-size: 18px;
  }

  .interaction-card__description {
    font-size: 12px;
  }

  .interaction-card__date {
    font-size: 10px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .interaction-card {
    transition: none;
  }

  .interaction-card:hover {
    transform: none;
  }
}

</style>
