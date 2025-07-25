from models.schemas import Dependency
from typing import List
import re

async def parse_requirements(file) -> List[Dependency]:
    content = await file.read()  # <- await aqui
    text = content.decode("utf-8")
    dependencies = []

    for line in text.splitlines():
        if "==" in line and not line.strip().startswith("#"):
            try:
                name, version = line.strip().split("==")
                dependencies.append(Dependency(name=name, version=version, ecosystem="PyPI"))
            except ValueError:
                continue  # ignora linhas malformada
    return dependencies
