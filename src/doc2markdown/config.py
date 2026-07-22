import os
from pathlib import Path

# -----------------------------
# Directorios del proyecto
# -----------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"
CHUNKS_DIR = OUTPUT_DIR / "chunks"
LOG_DIR = PROJECT_ROOT / "logs"

# -----------------------------
# Configuración
# -----------------------------

SUPPORTED_PDF = [".pdf"]

SUPPORTED_IMAGES = [
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".bmp",
    ".webp",
]

TESSERACT_CMD = os.environ.get("DOC2MD_TESSERACT_CMD")

RAG_MAX_PARAGRAPH_CHARS = 900