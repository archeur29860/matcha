import { defineStore } from "pinia";
import { ref } from "vue";

export const useUserStore = defineStore(
  'user',
  () => {
    const id = ref("")
    const email = ref("")
    const username = ref("")
    const first_name = ref("")
    const last_name = ref("")

    return {
      id,
      email,
      username,
      first_name,
      last_name
    }
  },
  {
    persist: true
  }
)
