from src.doc2markdown.controller import run
from src.doc2markdown.models import ConversionResult


def test_run_processes_pdf_and_images(monkeypatch, tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    pdf_file = input_dir / "archivo.pdf"
    image_file = input_dir / "imagen.jpg"
    ignored_file = input_dir / "nota.txt"

    pdf_file.write_text("dummy", encoding="utf-8")
    image_file.write_text("dummy", encoding="utf-8")
    ignored_file.write_text("dummy", encoding="utf-8")

    monkeypatch.setattr("src.doc2markdown.controller.INPUT_DIR", input_dir)
    monkeypatch.setattr("src.doc2markdown.controller.OUTPUT_DIR", output_dir)

    monkeypatch.setattr(
        "src.doc2markdown.controller.convert_pdf_to_markdown",
        lambda source: ConversionResult(
            success=True,
            input_file=source,
            markdown="PDF  \n\n\ncontenido",
            elapsed_time=0.1,
        ),
    )
    monkeypatch.setattr(
        "src.doc2markdown.controller.convert_image_to_markdown",
        lambda source: ConversionResult(
            success=True,
            input_file=source,
            markdown="IMG \n \ntexto",
            elapsed_time=0.1,
        ),
    )

    run()

    pdf_output = output_dir / "archivo.md"
    image_output = output_dir / "imagen.md"
    ignored_output = output_dir / "nota.md"

    assert pdf_output.exists()
    assert image_output.exists()
    assert not ignored_output.exists()
    assert pdf_output.read_text(encoding="utf-8") == "## PDF\n\ncontenido\n"
    assert image_output.read_text(encoding="utf-8") == "## IMG\n\ntexto\n"


def test_run_without_supported_files(monkeypatch, tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    (input_dir / "nota.txt").write_text("dummy", encoding="utf-8")

    monkeypatch.setattr("src.doc2markdown.controller.INPUT_DIR", input_dir)
    monkeypatch.setattr("src.doc2markdown.controller.OUTPUT_DIR", output_dir)

    run()

    assert list(output_dir.iterdir()) == []


def test_run_includes_metadata_block(monkeypatch, tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    image_file = input_dir / "imagen.jpg"
    image_file.write_text("dummy", encoding="utf-8")

    monkeypatch.setattr("src.doc2markdown.controller.INPUT_DIR", input_dir)
    monkeypatch.setattr("src.doc2markdown.controller.OUTPUT_DIR", output_dir)
    monkeypatch.setattr(
        "src.doc2markdown.controller.convert_image_to_markdown",
        lambda source: ConversionResult(
            success=True,
            input_file=source,
            markdown="Texto base",
            metadata={"archivo": source.name, "formato": "JPG"},
            elapsed_time=0.1,
        ),
    )

    run()

    output = (output_dir / "imagen.md").read_text(encoding="utf-8")

    assert "## Metadata" in output
    assert "- archivo: imagen.jpg" in output
    assert "- formato: JPG" in output
    assert "Texto base" in output