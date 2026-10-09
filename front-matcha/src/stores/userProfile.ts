import { defineStore } from "pinia";
import { ref } from "vue";

export const useUserProfileStore = defineStore(
  'user',
  () => {
    const id = ref("")
    const age = ref(0)
    const gender = ref("")
    const gender_pref = ref<string[]>([])
    const bio = ref("")
    const picture_profile_index = ref(0)
    const popularyty = ref(0)
    const location = ref("")
    const tags = ref<string[]>([])
    const pictures_paths = ref<string[]>([])

    return {
        id,
        age,
        gender,
        gender_pref,
        bio,
        picture_profile_index,
        popularyty,
        location,
        tags,
        pictures_paths
    }
},
{
    persist: false
}
)
