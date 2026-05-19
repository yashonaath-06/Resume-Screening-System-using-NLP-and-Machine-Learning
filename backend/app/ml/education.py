"""Education extractor based on a keyword corpus."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

_LEVEL_ORDER = [
    ("phd", ["phd", "ph.d", "doctorate", "doctor of philosophy", "post doc", "postdoctoral"]),
    ("masters", ["masters", "master's", "master of", "mba", "ms ", "m.s", "m.tech", "m.e", "m.sc", "mca"]),
    ("bachelors", ["bachelor", "bba", "b.tech", "b.e", "b.sc", "bca", "b.com"]),
    ("diploma", ["diploma", "associate degree"]),
    ("school", ["high school", "secondary school", "gcse", "a level", "intermediate",
                "hsc", "ssc", "12th", "10th"]),
]


def _load_keywords() -> List[str]:
    p = DATA_DIR / "education_keywords.txt"
    if not p.exists():
        return []
    return [
        line.strip().lower()
        for line in p.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


_KEYWORDS = _load_keywords()
_KEYWORDS.sort(key=len, reverse=True)


def extract_education(text: str) -> List[str]:
    if not text or not _KEYWORDS:
        return []
    t = text.lower()
    found: list[str] = []
    for kw in _KEYWORDS:
        # Loose match (no boundary issues with multi-word keywords)
        if kw in t and kw not in found:
            found.append(kw)
    return found


def highest_level(found: List[str]) -> str:
    """Map a list of education keywords to a canonical level."""
    found_l = [f.lower() for f in (found or [])]
    for level, markers in _LEVEL_ORDER:
        for m in markers:
            for f in found_l:
                if m.strip() in f:
                    return level
    return ""


_LEVEL_RANK = {"school": 1, "diploma": 2, "bachelors": 3, "masters": 4, "phd": 5, "": 0}


def meets_requirement(found: List[str], required: str) -> bool:
    if not required:
        return True
    have = highest_level(found)
    return _LEVEL_RANK.get(have, 0) >= _LEVEL_RANK.get(required.lower(), 0)
