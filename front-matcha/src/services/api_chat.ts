const URLAPI = "chat"

export async function send_message(chat_id:string, user_id:string, message:string){
    const response = await fetch(`http://localhost:5000/api/${URLAPI}/send/${chat_id}/`,{
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
        },
        body: JSON.stringify({
            from_user_id: user_id,
            message: message,
        }),
    });

    const data = await response.json();


    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
    }

    return data;
}


export async function get_chat(chat_id:string) {
    const response = await fetch(`http://localhost:5000/api/${URLAPI}/${chat_id}/`);

    const data = await response.json();

    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
    }

    return data;
}