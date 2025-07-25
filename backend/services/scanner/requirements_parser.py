from models.schemas import Dependency

def parse_requirements(text: str):
    dependencies = []
    for line in text.splitlines():
        if "==" in line and not line.strip().startswith("#"):
            name, version = line.strip().split("==")
            dependencies.append(Dependency(name=name, version=version))
    return dependencies
