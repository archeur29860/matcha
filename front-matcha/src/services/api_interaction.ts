import type { Interaction } from "@/types/interaction";

const URLAPI = 'interaction'

function mapInteractionType(data: any[]): Interaction[] {
    return data.map((row): Interaction => ({
        id: String(row.id),
        username: row.username,
        user_id: String(row.user_id),
        typeOfInter: row.which_interaction,
        created_at: row.created_at,
    }))
}

export async function new_iteraction(from_user:string, to_user:string, typeof_inter:string) {

    const response = await fetch(`http://localhost:5000/api/${URLAPI}/`, {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
        },
        body: JSON.stringify({
            from_user_id: from_user,
            to_user_id: to_user,
            which_interaction: typeof_inter,
        }),
    });

    const data = await response.json();
    
    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
    }
    
    return data;
}

export async function get_list_interaction_from(user_id:string, limit:number = 20, cursor:string = "") {
    const full_url = `http://localhost:5000/api/${URLAPI}/from/${user_id}/?limit=${limit}${cursor ? `&cursor=${cursor}` : ""}`;
    const response = await fetch(full_url);

    const data = await response.json();

    if (!response.ok) {
        console.error("Erreur HTTP:", response.status, data.error);
    }

    return mapInteractionType(data.data.items);
}

export async function get_list_interaction_to(user_id:string, limit:number = 20, cursor:string = "", typeof_inter:string = "") {
    const full_url = `http://localhost:5000/api/${URLAPI}/to/${user_id}/?limit=${limit}${cursor ? `&cursor=${cursor}` : ""}${typeof_inter ? `&typeof_inter=${typeof_inter}` : ""}`;
    const response = await fetch(full_url);

    const data = await response.json();

    if (!response.ok) {
        console.error("Erreur HTTP:", response.status, data.error);
    }

    return mapInteractionType(data.data.items);
}

export async function isLiked(from_user:string, to_user:string) {
    const full_url = `http://localhost:5000/api/${URLAPI}/${from_user}/${to_user}/`;
    const response = await fetch(full_url);

    const data = await response.json();

    if (!response.ok) {
        console.error("Erreur HTTP:", response.status, data.error);
    }

    return data;
}