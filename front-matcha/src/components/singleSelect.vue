<script setup lang="ts">
import Multiselect from 'vue-multiselect'

defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const options = ['Male', 'Female', 'Other']
function update(value: string | null) {
  if (value) emit('update:modelValue', value)
}
</script>

<template>
  <Multiselect
    :model-value="modelValue"
    @update:model-value="update"
    :options="options"
    :allow-empty="false"
    :searchable="false"
    placeholder="choose"
  />
</template>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>