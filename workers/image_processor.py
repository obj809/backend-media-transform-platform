import os
import time
from pathlib import Path

from PIL import Image

UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
PROCESSED_DIR = Path(__file__).parent.parent / "processed"
PROCESSED_DIR.mkdir(exist_ok=True)


def process_image(input_path: Path, output_path: Path) -> dict:
    """
    Process an image using Pillow.
    Currently converts to grayscale as an example transformation.
    """
    with Image.open(input_path) as img:
        # Example transformation: convert to grayscale
        processed = img.convert("L")
        processed.save(output_path, "JPEG", quality=85)

    return {
        "input": str(input_path),
        "output": str(output_path),
        "original_size": os.path.getsize(input_path),
        "processed_size": os.path.getsize(output_path),
    }


def process_pending_files() -> list[dict]:
    """
    Process all files in uploads folder that haven't been processed yet.
    """
    results = []

    for file_path in UPLOADS_DIR.glob("*.jpg"):
        output_filename = f"processed_{file_path.name}"
        output_path = PROCESSED_DIR / output_filename

        # Skip if already processed
        if output_path.exists():
            continue

        try:
            result = process_image(file_path, output_path)
            result["status"] = "success"
            results.append(result)
            print(f"Processed: {file_path.name} -> {output_filename}")
        except Exception as e:
            results.append({
                "input": str(file_path),
                "status": "error",
                "error": str(e),
            })
            print(f"Error processing {file_path.name}: {e}")

    return results


def run_worker(poll_interval: int = 5):
    """
    Run the worker continuously, polling for new files.
    """
    print(f"Starting image processor worker...")
    print(f"Watching: {UPLOADS_DIR}")
    print(f"Output: {PROCESSED_DIR}")

    while True:
        results = process_pending_files()
        if results:
            print(f"Processed {len(results)} file(s)")
        time.sleep(poll_interval)


if __name__ == "__main__":
    run_worker()
