import httpx
from typing import List, Dict
from schemas import Dependency

from cvss import CVSS4

import asyncio

cve_cache: Dict[str, dict] = {}

def classify_severity(score: float) -> str:
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    elif score > 0.0:
        return "Low"
    else:
        return "None"
    
def parse_requirements_and_scan(text: str):
    dependencies = []
    for line in text.splitlines():
        if "==" in line and not line.strip().startswith("#"):
            name, version = line.strip().split("==")
            dependencies.append(Dependency(name=name, version=version))
    return asyncio.run(scan_dependencies(dependencies))

    
async def fetch_cve_detail(vuln_id: str, client: httpx.AsyncClient) -> dict:
    if vuln_id in cve_cache:
        return cve_cache[vuln_id]

    try:
        resp = await client.get(f"https://api.osv.dev/v1/vulns/{vuln_id}")
        if resp.status_code == 200:
            data = resp.json()
            cve_cache[vuln_id] = data  # cache salva
            return data
    except Exception as e:
        print(f"Erro ao buscar {vuln_id}: {e}")

    return {}


async def scan_dependencies(dependencies: List[Dependency]):
    query_url = "https://api.osv.dev/v1/querybatch"

    queries = [
        {
            "package": {"name": dep.name, "ecosystem": "PyPI"},
            "version": dep.version
        }
        for dep in dependencies
    ]

    async with httpx.AsyncClient() as client:
        query_resp = await client.post(query_url, json={"queries": queries})
        results = []

        for dep, res in zip(dependencies, query_resp.json().get("results", [])):
            vulns = res.get("vulns", [])
            vuln_ids = [v.get("id") for v in vulns if v.get("id")]

            # faz as requisições paralelas
            detail_results = await asyncio.gather(*[
                fetch_cve_detail(v_id, client) for v_id in vuln_ids
            ])

            detailed_vulns = []

            for data in detail_results:
                if not data or "id" not in data:
                    continue

                severity = data.get("severity", [])
                cvss_v4_vector = next(
                    (s.get("score") for s in severity if s.get("type") == "CVSS_V4"), None
                )

                try:
                    if cvss_v4_vector:
                        cvss_obj = CVSS4(cvss_v4_vector)
                        score = cvss_obj.scores()["base"]
                        level = classify_severity(score)
                    else:
                        score = None
                        level = "Unknown"
                except Exception as e:
                    score = None
                    level = "Invalid vector"

                detailed_vulns.append({
                    "id": data.get("id"),
                    "summary": data.get("summary") or "No summary",
                    "details": data.get("details") or "No details",
                    "cvss_v4_vector": cvss_v4_vector,
                    "score": score,
                    "level": level,
                    "references": data.get("references", [])
                })

            results.append({
                "package": {"name": dep.name, "version": dep.version},
                "vulnerabilities": detailed_vulns
            })

        return results


def parse_requirements_and_scan(requirements_text: str):
    dependencies = []

    for line in requirements_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" in line:
            name, version = line.split("==")
            dependencies.append(Dependency(name=name.strip(), version=version.strip()))

    return scan_dependencies(dependencies)
