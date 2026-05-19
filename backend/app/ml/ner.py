"""NER + contact info extraction. Uses spaCy if available."""
from __future__ import annotations

import logging
import re
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\s().\-]{7,}\d)")
_NAME_LINE_RE = re.compile(r"^[A-Z][A-Za-z'\-]+(?:\s+[A-Z][A-Za-z'\-]+){1,3}$")


_nlp = None


def _get_nlp():
    global _nlp
    if _nlp is not None:
        return _nlp
    try:
        import spacy  # type: ignore
        try:
            _nlp = spacy.load("en_core_web_sm")
        except Exception:
            # Fallback: blank pipeline (no NER) so the app keeps running.
            _nlp = spacy.blank("en")
    except Exception as e:
        logger.warning("spaCy not available, NER disabled: %s", e)
        _nlp = False  # sentinel
    return _nlp


def extract_entities(text: str) -> Dict[str, List[str]]:
    """Return a mapping of entity label -> list of strings."""
    out: Dict[str, List[str]] = {}
    if not text:
        return out
    nlp = _get_nlp()
    if not nlp:
        return out
    try:
        doc = nlp(text[:200_000])  # cap for safety
        if hasattr(doc, "ents"):
            for ent in doc.ents:
                out.setdefault(ent.label_, []).append(ent.text.strip())
    except Exception as e:
        logger.warning("NER failed: %s", e)
    # Deduplicate while preserving order
    return {k: list(dict.fromkeys(v)) for k, v in out.items()}


def _guess_name_from_text(text: str, ents: Dict[str, List[str]]) -> str:
    persons = ents.get("PERSON") or []
    if persons:
        return persons[0]
    # Heuristic: first non-empty line that looks like a name.
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if _NAME_LINE_RE.match(line):
            return line
        # Stop scanning after first ~10 lines to avoid section headers.
        break
    return ""


def guess_name_email_phone(text: str, ents: Dict[str, List[str]]) -> Dict[str, str]:
    name = _guess_name_from_text(text, ents)
    email_match = _EMAIL_RE.search(text or "")
    phone_match = _PHONE_RE.search(text or "")
    return {
        "name": name,
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0).strip() if phone_match else "",
    }
