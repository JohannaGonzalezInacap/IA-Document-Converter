from src.doc2markdown.cleaner import clean_markdown


def test_clean_markdown_splits_glued_words_and_bullets():
    raw = (
        "ABProAprendizaje Basado en Proyectos\n"
        "Beneficios•Aprendizaje mas significativo•Desarrollo de habilidades"
    )

    cleaned = clean_markdown(raw)

    assert "## ABPro Aprendizaje Basado en Proyectos" in cleaned
    assert "## Beneficios" in cleaned
    assert "- Aprendizaje mas significativo" in cleaned
    assert "- Desarrollo de habilidades" in cleaned


def test_clean_markdown_splits_stage_and_slide_headers():
    raw = (
        "Proceso del ABPro ETAPA I: Lanzamiento del proyecto "
        "Diapositiva 1: Nombre del proyecto. Diapositiva 2: Objetivos."
    )

    cleaned = clean_markdown(raw)

    assert "\n## ETAPA I: Lanzamiento del proyecto" in cleaned
    assert "\n## Diapositiva 1: Nombre del proyecto." in cleaned
    assert "\n## Diapositiva 2: Objetivos." in cleaned


def test_clean_markdown_rebuilds_paragraphs():
    raw = (
        "Este es un texto\n"
        "que viene cortado en lineas\n"
        "sin separacion correcta.\n\n"
        "Segunda idea relacionada\n"
        "con el mismo tema"
    )

    cleaned = clean_markdown(raw)

    assert "Este es un texto que viene cortado en lineas sin separacion correcta." in cleaned
    assert "Segunda idea relacionada con el mismo tema" in cleaned


def test_clean_markdown_preserves_table_blocks():
    raw = (
        "| Nombre | Valor |\n"
        "| --- | --- |\n"
        "| A | 10 |\n"
        "| B | 20 |"
    )

    cleaned = clean_markdown(raw)

    assert "| Nombre | Valor |" in cleaned
    assert "| --- | --- |" in cleaned
    assert "| A | 10 |" in cleaned
    assert "| B | 20 |" in cleaned
