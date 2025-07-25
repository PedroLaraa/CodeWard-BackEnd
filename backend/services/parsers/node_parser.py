import json
import re
from typing import List, Dict
from models.schemas import Dependency

def clean_version(version_str: str) -> str:
    """
    Remove símbolos como ^, ~, >, < da versão.
    """
    return re.sub(r"^[^\d]*", "", version_str)

async def parse_package_json(file) -> List[Dict[str, str]]:
    content = await file.read()
    data = json.loads(content.decode("utf-8"))

    dependencies = []

    for section in ["dependencies", "devDependencies"]:
        deps = data.get(section, {})
        for name, version in deps.items():
            clean_ver = clean_version(version)
            dependencies.append(Dependency(name=name, version=clean_ver, ecosystem="npm"))

    return dependencies
