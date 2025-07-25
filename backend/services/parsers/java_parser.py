import xml.etree.ElementTree as ET
from typing import List, Dict
from fastapi import UploadFile
from models.schemas import Dependency

async def parse_pom_xml(file: UploadFile) -> List[Dict[str, str]]:
    content = await file.read()
    text = content.decode("utf-8")

    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []

    dependencies = []

    for dep in root.findall(".//dependency"):
        group_id = dep.findtext("groupId")
        artifact_id = dep.findtext("artifactId")
        version = dep.findtext("version")

        if group_id and artifact_id and version:
            package_name = f"{group_id}:{artifact_id}"
            dependencies.append(Dependency(name=package_name, version=version, ecosystem="Maven"))

    return dependencies
