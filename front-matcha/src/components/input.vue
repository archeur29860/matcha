<script setup lang="ts">
withDefaults(
  defineProps<{
    type?: string
    placeholder?: string
    disabled?: boolean
    id?: string
    ariaInvalid?: boolean
  }>(),
  { type: 'text', placeholder: '', disabled: false, id: undefined, ariaInvalid: false }
)

const model = defineModel<string>({ default: '' })
</script>

<template>
  <div class="input-wrapper">
    <input
      :id="id"
      :aria-invalid="ariaInvalid"
      v-model="model"
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
      class="input"
    />
  </div>
</template>

<style scoped>
.input-wrapper {
  width: 100%;
}

.input {
  width: 100%;
  height: 48px;
  padding: 0 16px;

  box-sizing: border-box;

  border: 1px solid #f1e5e5;
  border-radius: 14px;

  background: #ffffff;
  color: #3c2830;

  font-family: inherit;
  font-size: 15px;
  font-weight: 500;

  outline: none;

  box-shadow: 0 6px 18px rgba(60, 30, 40, 0.05);

  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    background 0.2s ease;
}

.input::placeholder {
  color: #b9a9af;
  font-weight: 400;
}

.input:hover:not(:disabled) {
  border-color: #ead5da;
}

.input:focus {
  border-color: #ed6284;
  box-shadow:
    0 0 0 3px rgba(237, 98, 132, 0.1),
    0 6px 18px rgba(60, 30, 40, 0.06);
}

.input:disabled {
  background: #f8f1f3;
  color: #a99aa0;
  cursor: not-allowed;
  box-shadow: none;
}

@media (max-width: 600px) {
  .input {
    height: 46px;
    font-size: 14px;
    padding: 0 14px;
  }
}
</style>
