import httpx
from typing import List
from schemas import Dependency

import httpx
from typing import List
from schemas import Dependency

def scan_dependencies(dependencies: List[Dependency]):
    query_url = "https://api.osv.dev/v1/querybatch"
    detail_url = "https://api.osv.dev/v1/vulns/"

    queries = [
        {
            "package": {"name": dep.name, "ecosystem": "PyPI"},
            "version": dep.version
        }
        for dep in dependencies
    ]

    query_resp = httpx.post(query_url, json={"queries": queries})
    results = []

    for dep, res in zip(dependencies, query_resp.json().get("results", [])):
        vulns = res.get("vulns", [])
        detailed_vulns = []

        for vuln in vulns:
            vuln_id = vuln.get("id")
            if not vuln_id:
                continue

            # agora busca os dados completos por ID
            detail_resp = httpx.get(f"{detail_url}{vuln_id}")
            if detail_resp.status_code != 200:
                continue

            data = detail_resp.json()

            detailed_vulns.append({
                "id": data.get("id"),
                "summary": data.get("summary") or "No summary",
                "details": data.get("details") or "No details",
                "severity": [
                    s.get("score") for s in data.get("severity", [])
                ] or ["N/A"],
                "cvss": data.get("cvss", {}),
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
