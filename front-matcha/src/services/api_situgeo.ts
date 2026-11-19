const URLAPI = 'situgeo'

export async function upsert_situgeo(
    user_id: string,
    gps_consent: boolean,
    lat?: number,
    lon?: number,
    label?: string
) {
    const response = await fetch(`http://localhost:5000/api/${URLAPI}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user_id: user_id,
            gps_consent: gps_consent,
            ...(lat !== undefined && lon !== undefined
                ? { lat: lat, lon: lon }
                : { label: label }),
        }),
    });

    const data = await response.json();

    if (!response.ok) {
        console.error('Erreur HTTP:', response.status, data.error);
        return;
    }

    return data;
}