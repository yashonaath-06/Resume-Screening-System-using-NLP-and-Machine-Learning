"""Experience extractor: estimate years of professional experience."""
from __future__ import annotations

import re
from datetime import datetime

# Patterns like "5 years", "5+ years", "5 yrs of experience"
_YEARS_RE = re.compile(
    r"(\d{1,2})\s*\+?\s*(?:years?|yrs?)(?:\s*(?:of)?\s*(?:experience|exp))?",
    re.IGNORECASE,
)

# Date ranges: "Jan 2019 - Mar 2022", "2019 - Present", "06/2020 - 09/2023"
_RANGE_RE = re.compile(
    r"(?P<s>(?:0?[1-9]|1[0-2])[/\-.](?:19|20)\d{2}|(?:19|20)\d{2}|"
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+(?:19|20)\d{2})"
    r"\s*[\-–—to]+\s*"
    r"(?P<e>(?:0?[1-9]|1[0-2])[/\-.](?:19|20)\d{2}|(?:19|20)\d{2}|"
    r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+(?:19|20)\d{2}|"
    r"present|current|now)",
    re.IGNORECASE,
)


_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _parse_date(s: str) -> tuple[int, int] | None:
    s = s.strip().lower()
    if s in {"present", "current", "now"}:
        now = datetime.utcnow()
        return now.year, now.month
    # numeric MM/YYYY or MM-YYYY
    m = re.match(r"^(\d{1,2})[/\-.](\d{4})$", s)
    if m:
        mo, yr = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12:
            return yr, mo
    # year only
    m = re.match(r"^(\d{4})$", s)
    if m:
        return int(m.group(1)), 6  # midyear assumption
    # "Jan 2020"
    m = re.match(r"^([a-z]{3,5})\.?\s+(\d{4})$", s)
    if m:
        mo = _MONTHS.get(m.group(1)[:3])
        if mo:
            return int(m.group(2)), mo
    return None


def estimate_experience_years(text: str) -> float:
    """Best-effort estimate of total professional experience in years."""
    if not text:
        return 0.0

    # 1) Explicit "N years experience" mentions
    explicit = 0.0
    for m in _YEARS_RE.finditer(text):
        try:
            n = float(m.group(1))
            explicit = max(explicit, n)
        except ValueError:
            continue

    # 2) Sum non-overlapping date ranges
    months_total = 0
    ranges: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for m in _RANGE_RE.finditer(text):
        s = _parse_date(m.group("s"))
        e = _parse_date(m.group("e"))
        if not s or not e:
            continue
        if (e[0], e[1]) < (s[0], s[1]):
            continue
        ranges.append((s, e))

    # Merge overlapping
    ranges.sort()
    merged: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for r in ranges:
        if merged and r[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], r[1]))
        else:
            merged.append(r)

    for (sy, sm), (ey, em) in merged:
        months_total += max(0, (ey - sy) * 12 + (em - sm))

    range_years = round(months_total / 12.0, 1)
    return float(max(explicit, range_years))
