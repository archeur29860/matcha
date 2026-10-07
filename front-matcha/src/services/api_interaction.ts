const URLAPI = 'interaction'

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
        return;
    }
    
    return data;
}

export async function get_list_interaction_from(user_id:string, limit:number = 20, cursor:string = "") {
    const full_url = `http://localhost:5000/api/${URLAPI}/from/${user_id}/?limit=${limit}${cursor ? `&cursor=${cursor}` : ""}`;
    const response = await fetch(full_url);

    const data = await response.json();

    if (!response.ok) {
        console.error("Erreur HTTP:", response.status, data.error);
        return;
    }

    return data;
}

export async function get_list_interaction_to(user_id:string, limit:number = 20, cursor:string = "") {
    const full_url = `http://localhost:5000/api/${URLAPI}/to/${user_id}/?limit=${limit}${cursor ? `&cursor=${cursor}` : ""}`;
    const response = await fetch(full_url);

    const data = await response.json();

    if (!response.ok) {
        console.error("Erreur HTTP:", response.status, data.error);
        return;
    }

    return data;
}