
<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  from_username: string
  to_username: string
  typeOfInter: string
  created_at: string | Date
}>()

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
</script>

<template>
  <article class="interaction-card">
    <span class="interaction-username" :title="from_username">
      {{ from_username }}
    </span>

    <span class="interaction-type" :title="typeOfInter">
      {{ typeOfInter }}
    </span>

    <span class="interaction-username" :title="to_username">
      {{ to_username }}
    </span>

    <time class="interaction-date" :datetime="new Date(created_at).toISOString()">
      {{ formattedDate }}
    </time>
  </article>
</template>

<style scoped>
.interaction-card {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fff;
  color: #1f2937;
  font-size: 14px;
}

.interaction-username {
  flex: 0 1 180px;
  min-width: 0;
  overflow: hidden;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.interaction-type {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  color: #4b5563;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.interaction-date {
  flex-shrink: 0;
  margin-left: auto;
  color: #6b7280;
  font-size: 12px;
  white-space: nowrap;
}

@media (max-width: 480px) {
  .interaction-card {
    gap: 8px;
    padding: 10px;
    font-size: 12px;
  }

  .interaction-username {
    flex-basis: 90px;
  }

  .interaction-date {
    font-size: 11px;
  }
}
</style>
