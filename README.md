# Backend Data Processing Engine

[![CI](https://github.com/obj809/backend-media-transform-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/obj809/backend-media-transform-platform/actions/workflows/ci.yml)

FastAPI service for JPG upload, grayscale image processing, and processed file download.

## Stack

- Python 3.12+
- FastAPI
- Uvicorn
- Pillow
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

- `GET /` - basic service response
- `GET /health` - health check
- `POST /upload` - upload JPG (max 25MB), processes to grayscale, stores in `processed/`
- `GET /download/{filename}` - download processed JPG

## Tests

```bash
pytest -v
```

## Notes

- CORS allows `http://localhost:3000`.
- Uploaded files are written to `uploads/`.
- Processed files are written to `processed/`.
