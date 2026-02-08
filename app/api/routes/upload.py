import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

UPLOADS_DIR = Path(__file__).parent.parent.parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    max_size = 25 * 1024 * 1024  # 25MB

    if file.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail="Only JPG files are allowed")

    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(status_code=413, detail="File size exceeds 25MB limit")

    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOADS_DIR / unique_filename

    # Save file to disk
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "filename": file.filename,
        "stored_filename": unique_filename,
        "size": len(contents),
        "content_type": file.content_type,
        "status": "uploaded"
    }
