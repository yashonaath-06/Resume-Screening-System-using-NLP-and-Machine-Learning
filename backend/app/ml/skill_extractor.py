"""Skill extractor backed by a curated skill corpus."""
from __future__ import annotations

import re
from pathlib import Path
from typing import List

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _load_skills() -> List[str]:
    p = DATA_DIR / "skills.txt"
    if not p.exists():
        return []
    skills = []
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip().lower()
        if s and not s.startswith("#"):
            skills.append(s)
    # Sort longest-first so multi-word skills win over single-word substrings.
    skills.sort(key=len, reverse=True)
    return skills


class SkillExtractor:
    def __init__(self) -> None:
        self.skills = _load_skills()
        # Pre-compile a single regex with word boundaries.
        # Special chars in skills (+, #, .) need escaping.
        escaped = [re.escape(s) for s in self.skills]
        # Word boundaries don't behave around + or #, so we use lookarounds.
        pattern = r"(?<![A-Za-z0-9])(?:" + "|".join(escaped) + r")(?![A-Za-z0-9])"
        self._re = re.compile(pattern, re.IGNORECASE) if escaped else None

    def extract(self, text: str) -> List[str]:
        if not text or self._re is None:
            return []
        found: list[str] = []
        seen: set[str] = set()
        for m in self._re.finditer(text):
            s = m.group(0).lower()
            if s not in seen:
                seen.add(s)
                found.append(s)
        return found

    def known_skills(self) -> List[str]:
        return list(self.skills)
