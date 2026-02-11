import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import pillow_heif

# Register HEIF/HEIC format with Pillow
pillow_heif.register_heif_opener()

router = APIRouter()

UPLOADS_DIR = Path(__file__).parent.parent.parent.parent / "uploads"
PROCESSED_DIR = Path(__file__).parent.parent.parent.parent / "processed"
UPLOADS_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)


def process_image(input_path: Path, output_path: Path):
    """Process image using Pillow - converts to RGB JPEG."""
    with Image.open(input_path) as img:
        processed = img.convert("RGB")
        processed.save(output_path, "JPEG", quality=85)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    max_size = 25 * 1024 * 1024  # 25MB

    allowed_types = ["image/jpeg", "image/png", "image/heic", "image/heif"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, and HEIC files are allowed")

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

    # Process the image (always output as JPG)
    unique_base = os.path.splitext(unique_filename)[0]
    processed_filename = f"processed_{unique_base}.jpg"
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
