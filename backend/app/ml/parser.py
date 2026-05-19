"""Resume file parser. Supports PDF, DOCX, TXT with graceful fallbacks."""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def _parse_pdf(path: str) -> str:
    try:
        import pdfplumber  # type: ignore
    except Exception as e:  # pragma: no cover
        logger.warning("pdfplumber not available: %s", e)
        return ""

    text_parts: list[str] = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                if t:
                    text_parts.append(t)
    except Exception as e:
        logger.warning("PDF parse failed for %s: %s", path, e)
    return "\n".join(text_parts)


def _parse_docx(path: str) -> str:
    try:
        from docx import Document  # type: ignore
    except Exception as e:  # pragma: no cover
        logger.warning("python-docx not available: %s", e)
        return ""

    try:
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text)
    except Exception as e:
        logger.warning("DOCX parse failed for %s: %s", path, e)
        return ""


def _parse_txt(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        logger.warning("TXT parse failed for %s: %s", path, e)
        return ""


def parse_resume_file(path: str, ext: str) -> str:
    """Return raw text extracted from a resume file."""
    ext = (ext or "").lower().lstrip(".")
    if ext == "pdf":
        return _parse_pdf(path)
    if ext == "docx":
        return _parse_docx(path)
    if ext == "txt":
        return _parse_txt(path)
    # Last resort: try as text
    return _parse_txt(path)
