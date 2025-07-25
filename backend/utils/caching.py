cve_cache = {}

def get_from_cache(vuln_id: str):
    return cve_cache.get(vuln_id)

def save_to_cache(vuln_id: str, data: dict):
    cve_cache[vuln_id] = data
