import httpx
from utils.caching import get_from_cache, save_to_cache

async def fetch_cve_detail(vuln_id: str, client: httpx.AsyncClient) -> dict:
    cached = get_from_cache(vuln_id)
    if cached:
        return cached

    try:
        resp = await client.get(f"https://api.osv.dev/v1/vulns/{vuln_id}")
        if resp.status_code == 200:
            data = resp.json()
            save_to_cache(vuln_id, data)
            return data
    except Exception as e:
        print(f"Erro ao buscar {vuln_id}: {e}")
    return {}
