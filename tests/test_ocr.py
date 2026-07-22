from pathlib import Path

import src.doc2markdown.ocr as ocr


def test_resolve_tesseract_cmd_from_path(monkeypatch):
    monkeypatch.setattr(ocr, "TESSERACT_CMD", None)
    monkeypatch.setattr(ocr.shutil, "which", lambda _name: r"C:\tools\tesseract.exe")

    resolved = ocr._resolve_tesseract_cmd()

    assert resolved == r"C:\tools\tesseract.exe"


def test_resolve_tesseract_cmd_from_windows_candidates(monkeypatch):
    monkeypatch.setattr(ocr, "TESSERACT_CMD", None)
    monkeypatch.setattr(ocr.shutil, "which", lambda _name: None)
    monkeypatch.setattr(
        ocr,
        "_WINDOWS_TESSERACT_CANDIDATES",
        [Path(r"C:\fake\tesseract.exe"), Path(r"C:\other\tesseract.exe")],
    )
    monkeypatch.setattr(Path, "exists", lambda self: str(self) == r"C:\other\tesseract.exe")

    resolved = ocr._resolve_tesseract_cmd()

    assert resolved == r"C:\other\tesseract.exe"
