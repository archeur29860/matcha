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

export async function get_userProfile_list(
  user_id: string,
  limit: number = 20,
  cursor: string | null = null
) {
  const params = new URLSearchParams({
    limit: String(limit),
  })

  if (cursor) {
    params.set('cursor', cursor)
  }

  const response = await fetch(
    `http://localhost:5000/api/${URLAPI}/list/${user_id}/?${params.toString()}`
  )

  const data = await response.json()

  if (!response.ok) {
    console.error('Erreur HTTP:', response.status, data.error)
    return data
  }

  return data
}