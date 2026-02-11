# Backend Data Processing Engine

[![CI](https://github.com/obj809/backend-media-transform-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/obj809/backend-media-transform-platform/actions/workflows/ci.yml)

FastAPI service for image upload (JPG, PNG, HEIC), processing, and download.

## Stack

- Python 3.12+
- FastAPI
- Uvicorn
- Pillow + pillow-heif
- Pytest

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API base URL: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Basic service response |
| `GET /health` | Health check |
| `POST /upload` | Upload image (JPG, PNG, HEIC; max 25MB), converts to JPG |
| `GET /download/{filename}` | Download processed JPG |

## Supported Formats

- **Input**: JPG, PNG, HEIC/HEIF
- **Output**: JPG (RGB color, 85% quality)

## Tests

```bash
pytest -v
```

## Notes

- CORS allows `http://localhost:3000`
- Original uploads stored in `uploads/` (preserves original format)
- Processed files stored in `processed/` (always JPG)

## TODO

- [ ] Database integration for file metadata and job tracking
- [ ] Redis queue for async job processing
- [ ] Separate worker container for image compression
