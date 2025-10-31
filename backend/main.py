from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from backend.models.schemas import Dependency
from backend.services.scanner.scan_executor import scan_dependencies
from backend.utils.detect_ecosystem import detect_ecosystem
from backend.api import auth

from fastapi.middleware.cors import CORSMiddleware

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)


app = FastAPI()
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://code-ward-nine.vercel.app/", "http://localhost:5173"],
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
    technology = await detect_ecosystem(file.filename.lower(), file)
    return await scan_dependencies(technology)
