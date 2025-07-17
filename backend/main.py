from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from schemas import Dependency
from scanner import scan_dependencies, parse_requirements_and_scan
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DependencyRequest(BaseModel):
    dependencies: list[Dependency]

@app.post("/scan")
async def scan(req: DependencyRequest):
    results = await scan_dependencies(req.dependencies)
    return results

@app.post("/scan-file")
async def scan_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    results = await parse_requirements_and_scan(text)
    return results
