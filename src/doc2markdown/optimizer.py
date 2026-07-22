import re
import unicodedata

from src.doc2markdown.config import RAG_MAX_PARAGRAPH_CHARS


_ONLY_PAGE_NUMBER = re.compile(r"^\d{1,4}$")
_MULTI_SPACE = re.compile(r"\s+")
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def _is_table_block(lines: list[str]) -> bool:
    return bool(lines) and all(line.strip().startswith("|") for line in lines)


def _is_list_block(lines: list[str]) -> bool:
    return bool(lines) and all(
        line.strip().startswith("- ") or re.match(r"^\d+[.)]\s+", line.strip())
        for line in lines
    )


def _split_long_sentence(sentence: str, max_chars: int) -> list[str]:
    words = sentence.split()
    if not words:
        return []

    chunks: list[str] = []
    current: list[str] = []

    for word in words:
        candidate = " ".join(current + [word]).strip()
        if len(candidate) <= max_chars:
            current.append(word)
            continue

        if current:
            chunks.append(" ".join(current).strip())
        current = [word]

    if current:
        chunks.append(" ".join(current).strip())

    return chunks


def _split_paragraph_for_rag(paragraph: str, max_chars: int) -> list[str]:
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(paragraph) if s.strip()]
    if not sentences:
        return []

    chunks: list[str] = []
    current = ""

    for sentence in sentences:
        sentence_parts = [sentence]
        if len(sentence) > max_chars:
            sentence_parts = _split_long_sentence(sentence, max_chars)

        for part in sentence_parts:
            candidate = part if not current else f"{current} {part}"
            if len(candidate) <= max_chars:
                current = candidate
                continue

            if current:
                chunks.append(current.strip())
            current = part

    if current:
        chunks.append(current.strip())

    return chunks


def optimize_markdown_for_rag(markdown: str, max_chars: int = RAG_MAX_PARAGRAPH_CHARS) -> str:
    normalized = unicodedata.normalize("NFC", markdown.replace("\r\n", "\n").replace("\r", "\n"))

    cleaned_lines: list[str] = []
    previous_non_empty: str | None = None

    for raw_line in normalized.split("\n"):
        line = raw_line.strip()

        if not line:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("")
            continue

        if _ONLY_PAGE_NUMBER.match(line):
            continue

        if line == previous_non_empty:
            continue

        cleaned_lines.append(line)
        previous_non_empty = line

    blocks: list[list[str]] = []
    block: list[str] = []

    for line in cleaned_lines:
        if line == "":
            if block:
                blocks.append(block)
                block = []
            continue
        block.append(line)

    if block:
        blocks.append(block)

    optimized_blocks: list[str] = []

    for block_lines in blocks:
        if _is_table_block(block_lines) or _is_list_block(block_lines):
            optimized_blocks.append("\n".join(block_lines))
            continue

        if len(block_lines) == 1 and block_lines[0].startswith("#"):
            optimized_blocks.append(block_lines[0])
            continue

        paragraph = _MULTI_SPACE.sub(" ", " ".join(block_lines)).strip()
        chunks = _split_paragraph_for_rag(paragraph, max_chars)
        optimized_blocks.extend(chunks or [paragraph])

    result = "\n\n".join(part.strip() for part in optimized_blocks if part.strip()).strip()
    if not result:
        return ""
    return f"{result}\n"


def split_markdown_into_chunks(markdown: str) -> list[str]:
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return blocks
