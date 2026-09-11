export async function apiFetch(url, options = {}) {
    
    const response = await fetch(url, options);
    
    const result = await response.json();
    
    if (!response.ok) {
        throw result.error;
    }
    
    return result.data;
}