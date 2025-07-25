import re
from typing import List, Dict
from fastapi import UploadFile
from models.schemas import Dependency

async def parse_build_gradle(file: UploadFile) -> List[Dict[str, str]]:
    content = await file.read()
    text = content.decode("utf-8")

    dependencies = []

    # Regex para capturar 'group:artifact:version'
    pattern = re.compile(r'["\']([\w\.-]+):([\w\.-]+):([\w\.-]+)["\']')

    for match in pattern.finditer(text):
        group = match.group(1)
        artifact = match.group(2)
        version = match.group(3)
        dependencies.append(Dependency(name=f"{group}:{artifact}", version=version, ecosystem="Maven"))

    return dependencies
