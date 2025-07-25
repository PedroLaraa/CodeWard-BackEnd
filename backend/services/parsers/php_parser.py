import json
import re
from typing import List, Dict
from fastapi import UploadFile
from models.schemas import Dependency

def clean_version(version_str: str) -> str:
    # Remove símbolos como ^, ~, >=, etc.
    return re.sub(r"^[^\d]*", "", version_str)

async def parse_composer_json(file: UploadFile) -> List[Dict[str, str]]:
    content = await file.read()
    data = json.loads(content.decode("utf-8"))

    packages = []

    for section in ["require", "require-dev"]:
        deps = data.get(section, {})
        for name, version in deps.items():
            clean_ver = clean_version(version)
            if clean_ver:  # Evita incluir pacotes sem versão válida
                packages.append(Dependency(name=name, version=clean_ver, ecosystem="Packagist"))

    return packages
