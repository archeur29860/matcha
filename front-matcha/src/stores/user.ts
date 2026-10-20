import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { socket } from "@/services/socket"

export const useUserStore = defineStore(
    'user',
    () => {
    const id = ref("")
    const email = ref("")
    const username = ref("")
    const first_name = ref("")
    const last_name = ref("")
    const age = ref("")
    const jwt = ref(localStorage.getItem("token") || "");

    const isAuthenticated = computed(() => !!jwt.value);

    function logout() {
        id.value = "";
        email.value = "";
        
        username.value = "";
        first_name.value = "";
        last_name.value = "";
        age.value = 0;

        jwt.value = "";
        socket.disconnect();
        localStorage.removeItem("token");
    }

    return {
      id,
      email,
      username,
      first_name,
      last_name,
      age
    }
    },
    {
    persist: true
    }
)