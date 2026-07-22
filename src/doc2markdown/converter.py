from io import BytesIO
from pathlib import Path
from time import perf_counter

from PIL import Image
from src.doc2markdown.models import ConversionResult
from src.doc2markdown.ocr import extract_text_from_image, extract_text_from_pil_image

def _build_error_result(
    input_file: Path,
    start_time: float,
    error: Exception,
) -> ConversionResult:
    elapsed = perf_counter() - start_time
    return ConversionResult(
        success=False,
        input_file=input_file,
        markdown="",
        error=f"{input_file.name}: {error}",
        elapsed_time=elapsed,
    )


def _convert_pdf_with_docling(pdf_path: Path) -> str:
    from docling.document_converter import DocumentConverter

    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    return result.document.export_to_markdown()


def _convert_pdf_with_pypdf(pdf_path: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    text = _extract_text_from_pdf_pages(reader)
    tables = _extract_tables_from_pdf(pdf_path)

    if text and tables:
        return f"{text}\n\n## Tablas detectadas\n\n{tables}"

    if text:
        return text

    if tables:
        return tables

    text_from_images = _extract_text_from_pdf_images(reader)

    if text_from_images:
        return text_from_images

    raise ValueError("No se pudo extraer texto del PDF.")


def _extract_text_from_pdf_pages(reader) -> str:
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(page.strip() for page in pages if page.strip())


def _extract_text_from_pdf_images(reader) -> str:
    extracted: list[str] = []

    for page in reader.pages:
        for image_data in getattr(page, "images", []):
            with Image.open(BytesIO(image_data.data)) as image:
                text = extract_text_from_pil_image(image)
                if text:
                    extracted.append(text)

    return "\n\n".join(extracted)


def _normalize_table_cell(cell: str | None) -> str:
    if cell is None:
        return ""
    return " ".join(cell.replace("\n", " ").split()).strip()


def _build_markdown_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""

    column_count = max(len(row) for row in rows)
    normalized_rows: list[list[str]] = []

    for row in rows:
        padded = row + [""] * (column_count - len(row))
        normalized_rows.append([_normalize_table_cell(cell) for cell in padded])

    header = normalized_rows[0]
    separator = ["---"] * column_count
    body = normalized_rows[1:] or [[""] * column_count]

    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in body)
    return "\n".join(lines)


def _extract_tables_from_pdf(pdf_path: Path) -> str:
    try:
        import pdfplumber
    except ImportError:
        return ""

    table_blocks: list[str] = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            for raw_table in page.extract_tables():
                if not raw_table:
                    continue

                rows = [row for row in raw_table if any(cell for cell in row if cell)]
                table_markdown = _build_markdown_table(rows)
                if table_markdown:
                    table_blocks.append(table_markdown)

    return "\n\n".join(table_blocks)


def _extract_pdf_metadata(pdf_path: Path) -> tuple[dict[str, str], int]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    raw_metadata = reader.metadata or {}
    page_count = len(reader.pages)

    metadata: dict[str, str] = {
        "archivo": pdf_path.name,
        "formato": "PDF",
        "paginas": str(page_count),
    }

    fields = {
        "/Title": "titulo",
        "/Author": "autor",
        "/Subject": "asunto",
        "/Creator": "creador",
        "/Producer": "productor",
    }

    for raw_key, normalized_key in fields.items():
        value = raw_metadata.get(raw_key)
        if value:
            metadata[normalized_key] = " ".join(str(value).split())

    return metadata, page_count


def _extract_image_metadata(image_path: Path) -> dict[str, str]:
    with Image.open(image_path) as image:
        metadata: dict[str, str] = {
            "archivo": image_path.name,
            "formato": image.format or image_path.suffix.replace(".", "").upper(),
            "ancho_px": str(image.width),
            "alto_px": str(image.height),
            "modo_color": image.mode,
        }

        dpi = image.info.get("dpi")
        if isinstance(dpi, tuple) and len(dpi) == 2:
            metadata["dpi"] = f"{dpi[0]}x{dpi[1]}"

    return metadata


def _build_image_description(metadata: dict[str, str]) -> str:
    width = int(metadata.get("ancho_px", "0"))
    height = int(metadata.get("alto_px", "0"))

    orientation = "cuadrada"
    if width > height:
        orientation = "horizontal"
    elif height > width:
        orientation = "vertical"

    color_mode = metadata.get("modo_color", "desconocido")
    fmt = metadata.get("formato", "imagen")
    dpi = metadata.get("dpi")

    description = (
        f"Imagen {orientation} en formato {fmt}, "
        f"de {width}x{height} px y modo de color {color_mode}."
    )
    if dpi:
        description += f" Resolucion registrada: {dpi} dpi."

    return description


def _text_to_markdown(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    non_empty_lines = [line for line in lines if line]
    return "\n".join(non_empty_lines)


def convert_pdf_to_markdown(pdf_path: Path) -> ConversionResult:

    start = perf_counter()

    try:
        metadata, page_count = _extract_pdf_metadata(pdf_path)

        try:
            markdown = _convert_pdf_with_docling(pdf_path)
        except ImportError:
            markdown = _text_to_markdown(_convert_pdf_with_pypdf(pdf_path))

        elapsed = perf_counter() - start

        return ConversionResult(
            success=True,
            input_file=pdf_path,
            markdown=markdown,
            pages=page_count,
            metadata=metadata,
            elapsed_time=elapsed,
        )

    except Exception as error:
        return _build_error_result(pdf_path, start, error)

def convert_image_to_markdown(image_path: Path) -> ConversionResult:
    start = perf_counter()

    try:
        metadata = _extract_image_metadata(image_path)
        text = extract_text_from_image(image_path)

        if not text:
            raise ValueError("No se pudo extraer texto de la imagen.")

        description = _build_image_description(metadata)
        extracted_text = _text_to_markdown(text)
        markdown = (
            "## Descripcion de imagen\n\n"
            f"{description}\n\n"
            "## Texto extraido\n\n"
            f"{extracted_text}"
        )
        elapsed = perf_counter() - start

        return ConversionResult(
            success=True,
            input_file=image_path,
            markdown=markdown,
            metadata=metadata,
            elapsed_time=elapsed,
        )

    except Exception as error:
        return _build_error_result(image_path, start, error)