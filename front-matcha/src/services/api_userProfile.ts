const URLAPI = "userprofile"

export async function get_userProfile(user_id:string) {
    const response = await fetch(`http://localhost:5000/api/${URLAPI}/${user_id}/`);

    const data = await response.json();

    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
        return data;
    }

    return data;
}