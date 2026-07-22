from src.doc2markdown.exporter import save_markdown
from src.doc2markdown.models import ConversionResult


def test_save_markdown(tmp_path):

    result = ConversionResult(
        success=True,
        input_file=tmp_path / "dummy.pdf",
        markdown="# Hola Mundo"
    )

    output_file = tmp_path / "archivo.md"

    save_markdown(result, output_file)

    assert output_file.exists()

    assert output_file.read_text(
        encoding="utf-8"
    ) == "# Hola Mundo"