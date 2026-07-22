from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ConversionResult:
    """
    Resultado de una conversión de documento.
    """

    success: bool

    input_file: Path

    markdown: str

    output_file: Path | None = None

    error: str | None = None

    pages: int | None = None

    metadata: dict[str, str] | None = None

    elapsed_time: float = 0.0