import shutil
from pathlib import Path

from PIL import Image
import pytesseract
from pytesseract import TesseractNotFoundError

from src.doc2markdown.config import TESSERACT_CMD


_WINDOWS_TESSERACT_CANDIDATES = [
    Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
    Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
]


def _resolve_tesseract_cmd() -> str | None:
    if TESSERACT_CMD:
        return TESSERACT_CMD

    in_path = shutil.which("tesseract")
    if in_path:
        return in_path

    for candidate in _WINDOWS_TESSERACT_CANDIDATES:
        if candidate.exists():
            return str(candidate)

    return None


def _configure_tesseract_cmd() -> None:
    resolved = _resolve_tesseract_cmd()
    if resolved:
        pytesseract.pytesseract.tesseract_cmd = resolved


def _run_tesseract(image: Image.Image) -> str:
    _configure_tesseract_cmd()

    try:
        return pytesseract.image_to_string(image, lang="spa+eng")
    except TesseractNotFoundError as error:
        raise RuntimeError(
            "Tesseract OCR no esta instalado o no esta en PATH. "
            "Instalalo o define DOC2MD_TESSERACT_CMD con la ruta completa "
            "a tesseract.exe."
        ) from error


def extract_text_from_image(image_path: Path) -> str:
    """
    Extrae texto de una imagen usando OCR.
    """

    with Image.open(image_path) as image:
        text = _run_tesseract(image)

    return text.strip()


def extract_text_from_pil_image(image: Image.Image) -> str:
    return _run_tesseract(image).strip()