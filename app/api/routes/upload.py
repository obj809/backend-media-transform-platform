import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image

router = APIRouter()

UPLOADS_DIR = Path(__file__).parent.parent.parent.parent / "uploads"
PROCESSED_DIR = Path(__file__).parent.parent.parent.parent / "processed"
UPLOADS_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)


def process_image(input_path: Path, output_path: Path):
    """Process image using Pillow - converts to grayscale."""
    with Image.open(input_path) as img:
        processed = img.convert("L")
        processed.save(output_path, "JPEG", quality=85)


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

    # Process the image
    processed_filename = f"processed_{unique_filename}"
    processed_path = PROCESSED_DIR / processed_filename
    process_image(file_path, processed_path)

    return {
        "filename": file.filename,
        "stored_filename": unique_filename,
        "processed_filename": processed_filename,
        "size": len(contents),
        "processed_size": os.path.getsize(processed_path),
        "content_type": file.content_type,
        "status": "processed"
    }
