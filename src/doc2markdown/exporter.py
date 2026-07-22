from pathlib import Path

from src.doc2markdown.models import ConversionResult


def save_markdown(result: ConversionResult, output_file: Path) -> None:
    """
    Guarda el Markdown generado por una conversión.
    """

    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        result.markdown,
        encoding="utf-8",
    )