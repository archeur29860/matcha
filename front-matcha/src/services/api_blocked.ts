const URLAPI = "blocked"

export async function block_user(user_id:string, user_id_blocked:string){
    const response = await fetch(`http://localhost:5000/api/${URLAPI}/`,{
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
        },
        body: JSON.stringify({
            user_id: user_id,
            user_id_blocked: user_id_blocked,
        }),
    });

    const data = await response.json();


    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
    }

    return data;
}

export async function remove_blocked_relation(user_id:string, user_id_blocked:string){
    const response = await fetch(`http://localhost:5000/api/${URLAPI}/`,{
        method: 'DELETE',
        headers: {
            'Content-Type':'application/json',
        },
        body: JSON.stringify({
            user_id: user_id,
            user_id_blocked: user_id_blocked,
        }),
    });

    const data = await response.json();

    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
    }

    return data;
}

export async function get_user_blocked_by(user_id:string){
    const response = await fetch(`http://localhost:5000/api/${URLAPI}/${user_id}/`);

    const data = await response.json();

    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
    }

    return data;
}