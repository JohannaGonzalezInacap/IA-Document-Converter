from pathlib import Path

from src.doc2markdown.config import INPUT_DIR, OUTPUT_DIR
from src.doc2markdown.cleaner import clean_markdown
from src.doc2markdown.converter import convert_image_to_markdown, convert_pdf_to_markdown
from src.doc2markdown.exporter import save_markdown
from src.doc2markdown.logger import setup_logger
from src.doc2markdown.optimizer import optimize_markdown_for_rag
from src.doc2markdown.utils import is_pdf, is_supported_document

logger = setup_logger()


def _find_supported_files() -> list[Path]:
    return sorted(
        file_path
        for file_path in INPUT_DIR.iterdir()
        if file_path.is_file() and is_supported_document(file_path)
    )


def _build_output_path(input_path: Path) -> Path:
    return OUTPUT_DIR / f"{input_path.stem}.md"


def _build_metadata_block(metadata: dict[str, str] | None) -> str:
    if not metadata:
        return ""

    lines = ["## Metadata"]
    lines.extend(f"- {key}: {value}" for key, value in metadata.items())
    return "\n".join(lines)


def run():

    OUTPUT_DIR.mkdir(exist_ok=True)

    files = _find_supported_files()

    if not files:

        logger.warning("No se encontraron archivos compatibles.")

        return

    logger.info("Se encontraron %d archivo(s).", len(files))

    total_time = 0

    for source_file in files:

        logger.info("=" * 60)
        logger.info("Procesando: %s", source_file.name)

        if is_pdf(source_file):
            result = convert_pdf_to_markdown(source_file)
        else:
            result = convert_image_to_markdown(source_file)

        total_time += result.elapsed_time

        if result.success:
            metadata_block = _build_metadata_block(result.metadata)
            markdown_with_metadata = result.markdown
            if metadata_block:
                markdown_with_metadata = f"{metadata_block}\n\n{result.markdown}"

            cleaned_markdown = clean_markdown(markdown_with_metadata)
            result.markdown = optimize_markdown_for_rag(cleaned_markdown)

            output = _build_output_path(source_file)

            save_markdown(result, output)

            logger.info(
                "Finalizado: %s (%.2f segundos)",
                source_file.name,
                result.elapsed_time,
            )

        else:

            logger.error(result.error)

    logger.info("=" * 60)
    logger.info("Tiempo total: %.2f segundos", total_time)
    logger.info("Proceso finalizado.")