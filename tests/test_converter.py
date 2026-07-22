from pathlib import Path

import src.doc2markdown.converter as converter
from src.doc2markdown.converter import (
    convert_image_to_markdown,
    convert_pdf_to_markdown,
)


def test_convert_pdf_with_pypdf_fallback(monkeypatch):
    test_pdf = Path("tests/resources/simple.pdf")

    def fake_docling(_pdf_path):
        raise ImportError("Docling no disponible")

    monkeypatch.setattr(
        "src.doc2markdown.converter._convert_pdf_with_docling",
        fake_docling,
    )
    monkeypatch.setattr(
        "src.doc2markdown.converter._convert_pdf_with_pypdf",
        lambda _pdf_path: "Linea 1\n\nLinea 2",
    )
    monkeypatch.setattr(
        "src.doc2markdown.converter._extract_pdf_metadata",
        lambda _pdf_path: ({"archivo": "simple.pdf", "formato": "PDF", "paginas": "1"}, 1),
    )

    result = convert_pdf_to_markdown(test_pdf)

    assert result.success
    assert result.markdown == "Linea 1\nLinea 2"
    assert result.input_file == test_pdf
    assert result.pages == 1
    assert result.metadata == {"archivo": "simple.pdf", "formato": "PDF", "paginas": "1"}
    assert result.elapsed_time >= 0


def test_convert_image_to_markdown(monkeypatch):
    test_image = Path("tests/resources/image.png")

    monkeypatch.setattr(
        "src.doc2markdown.converter.extract_text_from_image",
        lambda _image_path: "  Texto OCR  \n\nSegunda linea  ",
    )
    monkeypatch.setattr(
        "src.doc2markdown.converter._extract_image_metadata",
        lambda _image_path: {
            "archivo": "image.png",
            "formato": "PNG",
            "ancho_px": "1200",
            "alto_px": "800",
            "modo_color": "RGB",
        },
    )

    result = convert_image_to_markdown(test_image)

    assert result.success
    assert "## Descripcion de imagen" in result.markdown
    assert "Imagen horizontal en formato PNG, de 1200x800 px y modo de color RGB." in result.markdown
    assert "## Texto extraido" in result.markdown
    assert "Texto OCR\nSegunda linea" in result.markdown
    assert result.input_file == test_image
    assert result.metadata == {
        "archivo": "image.png",
        "formato": "PNG",
        "ancho_px": "1200",
        "alto_px": "800",
        "modo_color": "RGB",
    }


def test_convert_image_to_markdown_returns_error(monkeypatch):
    test_image = Path("tests/resources/image.png")

    def fake_ocr(_image_path):
        raise RuntimeError("Error de OCR")

    monkeypatch.setattr(
        "src.doc2markdown.converter.extract_text_from_image",
        fake_ocr,
    )
    monkeypatch.setattr(
        "src.doc2markdown.converter._extract_image_metadata",
        lambda _image_path: {"archivo": "image.png", "formato": "PNG"},
    )

    result = convert_image_to_markdown(test_image)

    assert not result.success
    assert "Error de OCR" in (result.error or "")


def test_convert_pdf_uses_ocr_when_text_is_missing(monkeypatch):
    class FakeReader:
        pages = []

    monkeypatch.setattr("pypdf.PdfReader", lambda _path: FakeReader())
    monkeypatch.setattr(
        "src.doc2markdown.converter._extract_text_from_pdf_pages",
        lambda _reader: "",
    )
    monkeypatch.setattr(
        "src.doc2markdown.converter._extract_text_from_pdf_images",
        lambda _reader: "Texto OCR PDF",
    )
    monkeypatch.setattr(
        "src.doc2markdown.converter._extract_tables_from_pdf",
        lambda _pdf_path: "",
    )

    text = converter._convert_pdf_with_pypdf(Path("dummy.pdf"))

    assert text == "Texto OCR PDF"


def test_convert_pdf_combines_text_and_tables(monkeypatch):
    class FakeReader:
        pages = []

    monkeypatch.setattr("pypdf.PdfReader", lambda _path: FakeReader())
    monkeypatch.setattr(
        "src.doc2markdown.converter._extract_text_from_pdf_pages",
        lambda _reader: "Contenido principal",
    )
    monkeypatch.setattr(
        "src.doc2markdown.converter._extract_tables_from_pdf",
        lambda _pdf_path: "| Columna |\n| --- |\n| Valor |",
    )

    text = converter._convert_pdf_with_pypdf(Path("dummy.pdf"))

    assert "Contenido principal" in text
    assert "## Tablas detectadas" in text
    assert "| Columna |" in text


def test_build_markdown_table():
    table = converter._build_markdown_table(
        [
            ["Nombre", "Valor"],
            ["A", "10"],
            ["B", "20"],
        ]
    )

    assert "| Nombre | Valor |" in table
    assert "| --- | --- |" in table
    assert "| A | 10 |" in table


def test_build_image_description():
    description = converter._build_image_description(
        {
            "formato": "JPG",
            "ancho_px": "600",
            "alto_px": "900",
            "modo_color": "RGB",
            "dpi": "300x300",
        }
    )

    assert "Imagen vertical en formato JPG" in description
    assert "de 600x900 px" in description
    assert "Resolucion registrada: 300x300 dpi." in description
