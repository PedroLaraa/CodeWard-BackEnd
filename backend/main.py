from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from models.schemas import Dependency
from services.scanner.scan_executor import scan_dependencies
from services.scanner.requirements_parser import parse_requirements

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DependencyRequest(BaseModel):
    dependencies: list[Dependency]

@app.post("/scan")
async def scan(req: DependencyRequest):
    return await scan_dependencies(req.dependencies)

@app.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    deps = parse_requirements(text)
    return await scan_dependencies(deps)
