import { useUserStore } from "@/stores/user";
const URLAPI = "connected";

export async function get_current_user(){
    const userStore = useUserStore()
    const response = await fetch(
        `http://localhost:5000/api/${URLAPI}/`,
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${userStore.jwt}`,
                "Content-Type": "application/json"
            }
        }
    );
    
    if (response.status === 401) {
        userStore.logout();
        throw new Error("Invalid token or expired session");
    }
    
    if (!response.ok) {
        throw new Error("Error profile");
    }
    
    const result = await response.json();
    console.log(result);
    return result
}