from src.doc2markdown.optimizer import optimize_markdown_for_rag


def test_optimize_markdown_for_rag_removes_page_numbers_and_duplicates():
    raw = "## Titulo\n\n1\n\nLinea util\n\nLinea util\n\n2\n"

    optimized = optimize_markdown_for_rag(raw)

    assert "## Titulo" in optimized
    assert "\n1\n" not in optimized
    assert "\n2\n" not in optimized
    assert optimized.count("Linea util") == 1


def test_optimize_markdown_for_rag_preserves_tables_and_lists():
    raw = (
        "- item uno\n"
        "- item dos\n\n"
        "| Columna | Valor |\n"
        "| --- | --- |\n"
        "| A | 10 |\n"
    )

    optimized = optimize_markdown_for_rag(raw)

    assert "- item uno" in optimized
    assert "| Columna | Valor |" in optimized
    assert "| --- | --- |" in optimized


def test_optimize_markdown_for_rag_splits_long_paragraph():
    raw = (
        "Primera frase corta. "
        "Segunda frase bastante larga para probar el particionado de parrafos. "
        "Tercera frase para cerrar."
    )

    optimized = optimize_markdown_for_rag(raw, max_chars=60)
    blocks = [b for b in optimized.strip().split("\n\n") if b]

    assert len(blocks) >= 2
    assert all(len(block) <= 60 for block in blocks)
