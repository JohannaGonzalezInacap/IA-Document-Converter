from pathlib import Path

from src.doc2markdown.config import SUPPORTED_IMAGES, SUPPORTED_PDF


def is_pdf(file_path: Path) -> bool:
    return file_path.suffix.lower() in SUPPORTED_PDF


def is_supported_image(file_path: Path) -> bool:
    return file_path.suffix.lower() in SUPPORTED_IMAGES


def is_supported_document(file_path: Path) -> bool:
    return is_pdf(file_path) or is_supported_image(file_path)