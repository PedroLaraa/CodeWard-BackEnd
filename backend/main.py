from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from schemas import Dependency
from scanner import scan_dependencies, parse_requirements_and_scan

app = FastAPI()

class DependencyRequest(BaseModel):
    dependencies: list[Dependency]

@app.post("/scan")
def scan(req: DependencyRequest):
    results = scan_dependencies(req.dependencies)
    return results

@app.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    results = parse_requirements_and_scan(text)
    return results
