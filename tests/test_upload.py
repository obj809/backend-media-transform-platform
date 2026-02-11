import os
from pathlib import Path
from io import BytesIO

import pytest
from PIL import Image

UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
PROCESSED_DIR = Path(__file__).parent.parent / "processed"


def create_test_jpeg():
    """Create a valid JPEG image in memory"""
    img = Image.new("RGB", (100, 100), color="red")
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer.read()


def test_upload_jpg_success(client):
    """Test successful JPG file upload"""
    file_content = create_test_jpeg()
    response = client.post(
        "/upload",
        files={"file": ("test.jpg", BytesIO(file_content), "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.jpg"
    assert data["status"] == "processed"
    assert data["content_type"] == "image/jpeg"
    assert data["size"] == len(file_content)
    assert "stored_filename" in data
    assert "processed_filename" in data

    # Clean up: remove uploaded and processed files
    stored_file = UPLOADS_DIR / data["stored_filename"]
    processed_file = PROCESSED_DIR / data["processed_filename"]
    if stored_file.exists():
        stored_file.unlink()
    if processed_file.exists():
        processed_file.unlink()


def test_upload_file_saved_to_disk(client):
    """Test that uploaded file is saved to disk"""
    file_content = create_test_jpeg()
    response = client.post(
        "/upload",
        files={"file": ("image.jpg", BytesIO(file_content), "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()

    stored_file = UPLOADS_DIR / data["stored_filename"]
    processed_file = PROCESSED_DIR / data["processed_filename"]
    assert stored_file.exists()
    assert processed_file.exists()

    with open(stored_file, "rb") as f:
        saved_content = f.read()
    assert saved_content == file_content

    # Clean up
    stored_file.unlink()
    processed_file.unlink()


def create_test_png():
    """Create a valid PNG image in memory"""
    img = Image.new("RGB", (100, 100), color="blue")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.read()


def test_upload_png_success(client):
    """Test successful PNG file upload"""
    file_content = create_test_png()
    response = client.post(
        "/upload",
        files={"file": ("test.png", BytesIO(file_content), "image/png")}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.png"
    assert data["status"] == "processed"
    assert data["content_type"] == "image/png"
    assert data["processed_filename"].endswith(".jpg")

    # Clean up
    (UPLOADS_DIR / data["stored_filename"]).unlink()
    (PROCESSED_DIR / data["processed_filename"]).unlink()


def test_upload_rejects_unsupported_type(client):
    """Test that unsupported file types are rejected"""
    response = client.post(
        "/upload",
        files={"file": ("test.gif", BytesIO(b"fake gif"), "image/gif")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only JPG, PNG, and HEIC files are allowed"


def test_upload_rejects_pdf(client):
    """Test that PDF files are rejected"""
    response = client.post(
        "/upload",
        files={"file": ("doc.pdf", BytesIO(b"fake pdf"), "application/pdf")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only JPG, PNG, and HEIC files are allowed"


def test_upload_unique_filenames(client):
    """Test that each upload gets a unique filename"""
    file_content = create_test_jpeg()

    response1 = client.post(
        "/upload",
        files={"file": ("same.jpg", BytesIO(file_content), "image/jpeg")}
    )
    response2 = client.post(
        "/upload",
        files={"file": ("same.jpg", BytesIO(file_content), "image/jpeg")}
    )

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    assert data1["stored_filename"] != data2["stored_filename"]

    # Clean up
    (UPLOADS_DIR / data1["stored_filename"]).unlink()
    (UPLOADS_DIR / data2["stored_filename"]).unlink()
    (PROCESSED_DIR / data1["processed_filename"]).unlink()
    (PROCESSED_DIR / data2["processed_filename"]).unlink()


def test_upload_no_file(client):
    """Test upload without file"""
    response = client.post("/upload")
    assert response.status_code == 422
