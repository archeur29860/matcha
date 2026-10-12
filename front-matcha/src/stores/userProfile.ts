import { defineStore } from "pinia";
import { ref } from "vue";

interface Tag {
  id: string
  label: string
}

interface Picture {
  id: number
  url: string
}

export const useUserProfileStore = defineStore(
  'userProfile',
  () => {
    const id = ref("")
    const username = ref("")
    const first_name = ref("")
    const last_name = ref("")
    const last_connection = ref<string | null>(null);
    const age = ref(0)
    const gender = ref("")
    const gender_pref = ref<string[]>([])
    const bio = ref("")
    const picture_profile_index = ref(0)
    const popularity = ref(0)
    const location = ref("")
    const tags = ref<Tag[]>([])
    const pictures = ref<Picture[]>([])

    return {
        id,
        username,
        first_name,
        last_name,
        last_connection,
        age,
        gender,
        gender_pref,
        bio,
        picture_profile_index,
        popularity,
        location,
        tags,
        pictures
    }
},
{
    persist: false
}
)
