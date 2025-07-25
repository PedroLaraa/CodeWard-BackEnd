import re
from typing import List, Dict
from fastapi import UploadFile
from models.schemas import Dependency

def clean_version(version_str: str) -> str:
    return re.sub(r"^[^\d]*", "", version_str)

async def parse_gemfile(file: UploadFile) -> List[Dict[str, str]]:
    content = await file.read()
    text = content.decode("utf-8")

    dependencies = []
    for line in text.splitlines():
        if line.strip().startswith("gem"):
            match = re.match(r"gem ['\"]([^'\"]+)['\"](?:,\s*['\"]([^'\"]+)['\"])?", line.strip())
            if match:
                name = match.group(1)
                version = match.group(2) or "unknown"
                dependencies.append(Dependency(name=name, version=clean_version(version), ecosystem="RubyGems"))

    return dependencies
