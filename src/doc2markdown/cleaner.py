import re


_THREE_PLUS_BLANK_LINES = re.compile(r"\n{3,}")
_LOWER_UPPER_BOUNDARY = re.compile(r"([a-záéíóúñ])([A-ZÁÉÍÓÚÑ])")
_PUNCTUATION_WITHOUT_SPACE = re.compile(r"([,;:!?])([A-Za-zÁÉÍÓÚÜÑáéíóúüñ])")
_BULLET_MARKERS = re.compile(r"\s*[•§]\s*")
_STAGE_HEADERS = re.compile(r"(?<!\n)(ETAPA\s+[IVX]+(?:\s*:\s*|\s+))")
_SLIDE_HEADERS = re.compile(r"(?<!\n)(Diapositiva\s+\d+\s*:)")
_MULTI_SPACE_SEPARATOR = re.compile(r"\s{2,}")
_ORDERED_LIST = re.compile(r"^\d+[.)]\s+")
_TITLE_PREFIXES = ("ETAPA ", "Etapa ", "Diapositiva ", "Rúbrica")


def _break_long_line(line: str, threshold: int = 180) -> str:
    if len(line) <= threshold:
        return line
    return re.sub(r"\.\s+", ".\n", line)


def _is_list_item(line: str) -> bool:
    return line.startswith("- ") or bool(_ORDERED_LIST.match(line))


def _is_heading_candidate(line: str) -> bool:
    stripped = line.strip()

    if not stripped:
        return False

    if _is_list_item(stripped):
        return False

    if stripped.startswith("#"):
        return False

    if stripped.startswith(_TITLE_PREFIXES):
        return True

    if len(stripped) > 80:
        return False

    if stripped[-1] in ".;!?":
        return False

    words = stripped.split()
    if not words or len(words) > 10:
        return False

    alpha_words = [word for word in words if any(char.isalpha() for char in word)]
    if not alpha_words:
        return False

    titled = sum(1 for word in alpha_words if word[0].isupper())
    return (titled / len(alpha_words)) >= 0.6


def _is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def _to_candidate_lines(normalized: str) -> list[str]:
    candidates: list[str] = []

    for raw_line in normalized.split("\n"):
        trimmed = raw_line.strip()
        if not trimmed:
            candidates.append("")
            continue

        if _is_table_row(trimmed):
            candidates.append(trimmed)
            continue

        split_by_space = _MULTI_SPACE_SEPARATOR.sub("\n", trimmed)
        split_by_length = _break_long_line(split_by_space)

        for part in split_by_length.split("\n"):
            chunk = part.strip()
            if chunk:
                candidates.append(chunk)

    return candidates


def _build_markdown_blocks(lines: list[str]) -> str:
    blocks: list[str] = []
    paragraph_parts: list[str] = []
    list_parts: list[str] = []
    table_parts: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_parts:
            blocks.append(" ".join(paragraph_parts).strip())
            paragraph_parts.clear()

    def flush_list() -> None:
        if list_parts:
            blocks.append("\n".join(list_parts))
            list_parts.clear()

    def flush_table() -> None:
        if table_parts:
            blocks.append("\n".join(table_parts))
            table_parts.clear()

    for line in lines:
        if not line:
            flush_paragraph()
            flush_list()
            flush_table()
            continue

        if _is_heading_candidate(line):
            flush_paragraph()
            flush_list()
            flush_table()
            heading = line if line.startswith("#") else f"## {line}"
            blocks.append(heading)
            continue

        if _is_list_item(line):
            flush_paragraph()
            flush_table()
            list_parts.append(line)
            continue

        if _is_table_row(line):
            flush_paragraph()
            flush_list()
            table_parts.append(line)
            continue

        flush_list()
        flush_table()
        paragraph_parts.append(line)

    flush_paragraph()
    flush_list()
    flush_table()

    return "\n\n".join(block for block in blocks if block.strip())


def clean_markdown(markdown: str) -> str:
    """
    Normaliza el Markdown para reducir ruido y consumo de tokens.
    """

    normalized = markdown.replace("\r\n", "\n").replace("\r", "\n")
    normalized = _LOWER_UPPER_BOUNDARY.sub(r"\1 \2", normalized)
    normalized = _PUNCTUATION_WITHOUT_SPACE.sub(r"\1 \2", normalized)
    normalized = _BULLET_MARKERS.sub("\n- ", normalized)
    normalized = _STAGE_HEADERS.sub(r"\n\1", normalized)
    normalized = _SLIDE_HEADERS.sub(r"\n\1", normalized)
    normalized_lines = _to_candidate_lines(normalized)
    normalized = _build_markdown_blocks(normalized_lines)
    normalized = _THREE_PLUS_BLANK_LINES.sub("\n\n", normalized)
    normalized = normalized.strip()

    if normalized:
        return f"{normalized}\n"

    return ""