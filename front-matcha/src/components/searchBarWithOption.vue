<script setup lang="ts">
import { computed, ref } from 'vue'

export interface SearchOption {
  id: string
  label: string
  subtitle?: string
  image?: string
}

const props = withDefaults(
  defineProps<{
    options?: SearchOption[]
    placeholder?: string
  }>(),
  {
    options: () => [],
    placeholder: 'Rechercher...',
  }
)

const emit = defineEmits<{
  select: [option: SearchOption]
}>()

const search = ref('')
const isFocused = ref(false)

const filteredOptions = computed(() => {
  const query = search.value.trim().toLowerCase()

  if (!query) {
    return []
  }

  return (props.options ?? [])
    .filter((option) => {
      return (
        option.label.toLowerCase().includes(query) ||
        (option.subtitle?.toLowerCase().includes(query) ?? false)
      )
    })
    .slice(0, 8)
})

const showOptions = computed(() => {
  return (
    isFocused.value &&
    search.value.trim().length > 0 &&
    filteredOptions.value.length > 0
  )
})

function selectOption(option: SearchOption) {
  search.value = option.label
  isFocused.value = false

  emit('select', option)
}

function clearSearch() {
  search.value = ''
}

function handleBlur() {
  // Petit délai pour permettre au click sur une option
  // d'être traité avant de fermer la liste.
  setTimeout(() => {
    isFocused.value = false
  }, 100)
}
</script>

<template>
  <div class="search-bar">
    <!-- Recherche -->
    <div
      class="search-bar__input-wrapper"
      :class="{
        'search-bar__input-wrapper--focused': isFocused
      }"
    >
      <span class="search-bar__icon">
        ⌕
      </span>

      <input
        v-model="search"
        type="text"
        :placeholder="placeholder"
        class="search-bar__input"
        autocomplete="off"
        @focus="isFocused = true"
        @blur="handleBlur"
      />

      <button
        v-if="search"
        type="button"
        class="search-bar__clear"
        aria-label="Effacer la recherche"
        @mousedown.prevent="clearSearch"
      >
        ×
      </button>
    </div>

    <!-- Liste des résultats -->
    <Transition name="search-options">
      <div
        v-if="showOptions"
        class="search-bar__options"
      >
        <button
          v-for="option in filteredOptions"
          :key="option.id"
          type="button"
          class="search-bar__option"
          @mousedown.prevent="selectOption(option)"
        >
          <!-- Image -->
          <div
            v-if="option.image"
            class="search-bar__option-image"
          >
            <img
              :src="'http://localhost:5000/api/pictures/' + option.image"
              :alt="option.label"
            />
          </div>

          <div
            v-else
            class="search-bar__option-placeholder"
          >
            {{ option.label.charAt(0).toUpperCase() }}
          </div>

          <!-- Informations -->
          <div class="search-bar__option-content">
            <strong>
              {{ option.label }}
            </strong>

            <span v-if="option.subtitle">
              {{ option.subtitle }}
            </span>
          </div>

          <span class="search-bar__option-arrow">
            →
          </span>
        </button>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.search-bar {
  position: relative;
  width: 100%;
  max-width: 500px;
}

/* =========================================
   INPUT
========================================= */

.search-bar__input-wrapper {
  display: flex;
  align-items: center;

  width: 100%;
  height: 50px;

  padding: 0 14px;

  background: #ffffff;

  border: 1px solid #f1e5e5;
  border-radius: 16px;

  box-shadow: 0 6px 20px rgba(60, 30, 40, 0.06);

  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.search-bar__input-wrapper:hover {
  border-color: #f0cbd4;
}

.search-bar__input-wrapper--focused {
  border-color: #ed6284;

  box-shadow:
    0 0 0 3px rgba(237, 98, 132, 0.1),
    0 8px 24px rgba(60, 30, 40, 0.08);
}

.search-bar__icon {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 25px;
  margin-right: 8px;

  color: #b85570;
  font-size: 23px;
}

.search-bar__input {
  flex: 1;

  min-width: 0;

  border: 0;
  outline: 0;

  color: #302329;
  background: transparent;

  font: inherit;
  font-size: 14px;
}

.search-bar__input::placeholder {
  color: #a9979d;
}

.search-bar__clear {
  display: flex;
  align-items: center;
  justify-content: center;

  width: 28px;
  height: 28px;

  padding: 0;

  border: 0;
  border-radius: 50%;

  color: #8b777d;
  background: #f8f1f3;

  font-size: 20px;
  line-height: 1;

  cursor: pointer;

  transition:
    color 0.2s ease,
    background 0.2s ease;
}

.search-bar__clear:hover {
  color: #b85570;
  background: #fff0f3;
}

/* =========================================
   OPTIONS
========================================= */

.search-bar__options {
  position: absolute;
  z-index: 100;

  top: calc(100% + 8px);
  left: 0;
  right: 0;

  overflow: hidden;

  padding: 6px;

  background: #ffffff;

  border: 1px solid #f1e5e5;
  border-radius: 18px;

  box-shadow: 0 14px 35px rgba(60, 30, 40, 0.12);
}

.search-bar__option {
  display: flex;
  align-items: center;

  width: 100%;

  gap: 12px;

  padding: 10px;

  border: 0;
  border-radius: 13px;

  text-align: left;

  background: transparent;

  cursor: pointer;

  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.search-bar__option:hover {
  background: #fff1f4;
}

.search-bar__option:active {
  transform: scale(0.99);
}

/* =========================================
   OPTION IMAGE
========================================= */

.search-bar__option-image,
.search-bar__option-placeholder {
  width: 42px;
  height: 42px;

  flex-shrink: 0;

  overflow: hidden;

  border-radius: 12px;
}

.search-bar__option-image {
  background: #f8eeee;
}

.search-bar__option-image img {
  width: 100%;
  height: 100%;

  display: block;

  object-fit: cover;
}

.search-bar__option-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;

  color: #b85570;
  background: #fff0f3;

  font-size: 17px;
  font-weight: 700;
}

/* =========================================
   OPTION CONTENT
========================================= */

.search-bar__option-content {
  min-width: 0;

  display: flex;
  flex: 1;
  flex-direction: column;

  gap: 3px;
}

.search-bar__option-content strong {
  overflow: hidden;

  color: #302329;

  font-size: 14px;
  font-weight: 700;

  white-space: nowrap;
  text-overflow: ellipsis;
}

.search-bar__option-content span {
  overflow: hidden;

  color: #8b777d;

  font-size: 12px;

  white-space: nowrap;
  text-overflow: ellipsis;
}

.search-bar__option-arrow {
  color: #c58a99;
  font-size: 18px;

  transition: transform 0.2s ease;
}

.search-bar__option:hover .search-bar__option-arrow {
  transform: translateX(3px);
}

/* =========================================
   TRANSITION
========================================= */

.search-options-enter-active,
.search-options-leave-active {
  transition:
    opacity 0.15s ease,
    transform 0.15s ease;
}

.search-options-enter-from,
.search-options-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

/* =========================================
   MOBILE
========================================= */

@media (max-width: 600px) {
  .search-bar {
    max-width: 100%;
  }

  .search-bar__input-wrapper {
    height: 48px;
    border-radius: 14px;
  }

  .search-bar__options {
    top: calc(100% + 6px);
    border-radius: 16px;
  }

  .search-bar__option {
    padding: 9px;
  }
}
</style>