from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

PROCESSED_DIR = Path(__file__).parent.parent.parent.parent / "processed"


@router.get("/download/{filename}")
async def download_file(filename: str):
    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="image/jpeg"
    )
