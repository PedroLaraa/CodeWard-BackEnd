from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from models.schemas import Dependency
from services.scanner.scan_executor import scan_dependencies
from services.parsers.python_parser import parse_requirements
from utils.detect_ecosystem import detect_ecosystem

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
    technology = await detect_ecosystem(file.filename, file)
    print(technology)
    return await scan_dependencies(technology)
