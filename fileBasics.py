import os
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

app = FastAPI()

UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {
        "message": f"File '{filename}' uploaded successfully",
        "file_path": f"/files/{filename}",
    }


@app.get("/get_files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": f"File '{filename}' found", "file_path": f"/files/{filename}"}
