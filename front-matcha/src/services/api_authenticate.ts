const URLAPI = "auth"

export async function login(email:string, password:string, JWT: string){
        const response = await fetch(`http://localhost:5000/api/${URLAPI}/`,{
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
        }),
    });

    const data = await response.json();


    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
        return data;
    }

    return data;
}