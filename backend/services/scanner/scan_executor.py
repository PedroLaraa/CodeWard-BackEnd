import asyncio
import httpx
from typing import List
from models.schemas import Dependency
from cvss import CVSS4, CVSS3
from services.enrichers.cve_enricher import fetch_cve_detail
from services.classifiers.severity_classifier import classify_severity

async def scan_dependencies(dependencies: List[Dependency]):
    query_url = "https://api.osv.dev/v1/querybatch"

    queries = [
        {"package": {"name": dep.name, "ecosystem": "PyPI"}, "version": dep.version}
        for dep in dependencies
    ]

    async with httpx.AsyncClient() as client:
        query_resp = await client.post(query_url, json={"queries": queries})
        results = []

        for dep, res in zip(dependencies, query_resp.json().get("results", [])):
            vulns = res.get("vulns", [])
            vuln_ids = [v.get("id") for v in vulns if v.get("id")]

            detail_results = await asyncio.gather(*[
                fetch_cve_detail(v_id, client) for v_id in vuln_ids
            ])

            detailed_vulns = []
            for data in detail_results:
                if not data or "id" not in data:
                    continue

                severity = data.get("severity", [])
                cvss_v4 = next((s.get("score") for s in severity if s.get("type") == "CVSS_V4"), None)
                cvss_v3 = next((s.get("score") for s in severity if s.get("type") == "CVSS_V3"), None)

                try:
                    if cvss_v4:
                        score = CVSS4(cvss_v4).scores()[0]
                        level = classify_severity(score)
                    elif cvss_v3:
                        score = CVSS3(cvss_v3).scores()[0]
                        level = classify_severity(score)
                    else:
                        score = None
                        level = "Unknown"
                except:
                    score = None
                    level = "Invalid vector"

                detailed_vulns.append({
                    "id": data.get("id"),
                    "summary": data.get("summary") or "No summary",
                    "details": data.get("details") or "No details",
                    "cvss_v4_vector": cvss_v4,
                    "score": score,
                    "level": level,
                    "references": data.get("references", [])
                })

            results.append({
                "package": {"name": dep.name, "version": dep.version},
                "vulnerabilities": detailed_vulns
            })

        return results
