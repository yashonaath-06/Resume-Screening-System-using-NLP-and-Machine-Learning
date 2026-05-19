"""Text cleaning and tokenization with NLTK fallback to pure Python."""
from __future__ import annotations

import re
from typing import List

# A sensible English stopword set used as a fallback.
_FALLBACK_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "else", "for", "to",
    "of", "in", "on", "at", "by", "with", "from", "as", "is", "are", "was",
    "were", "be", "been", "being", "this", "that", "these", "those", "it",
    "its", "i", "you", "he", "she", "we", "they", "them", "his", "her",
    "their", "our", "my", "me", "your", "yours", "do", "does", "did", "have",
    "has", "had", "having", "will", "would", "should", "can", "could", "may",
    "might", "must", "about", "into", "over", "under", "between", "through",
    "while", "during", "after", "before", "above", "below", "than", "so",
    "such", "no", "not", "only", "own", "same", "very", "s", "t", "just",
    "also", "etc", "via", "per",
}

_WS_RE = re.compile(r"\s+")
_NON_ALNUM_RE = re.compile(r"[^a-z0-9+#./\- ]")
_URL_RE = re.compile(r"https?://\S+|www\.\S+")
_EMAIL_RE = re.compile(r"\S+@\S+\.\S+")
_PHONE_RE = re.compile(r"(?:\+?\d[\d\s().\-]{7,}\d)")


def _get_stopwords() -> set[str]:
    try:
        from nltk.corpus import stopwords  # type: ignore
        return set(stopwords.words("english"))
    except Exception:
        return set(_FALLBACK_STOPWORDS)


_STOPWORDS = _get_stopwords()


def clean_text(text: str) -> str:
    """Lowercase, strip URLs/emails/phones, collapse whitespace, remove odd chars."""
    if not text:
        return ""
    t = text.lower()
    t = _URL_RE.sub(" ", t)
    t = _EMAIL_RE.sub(" ", t)
    t = _PHONE_RE.sub(" ", t)
    t = _NON_ALNUM_RE.sub(" ", t)
    t = _WS_RE.sub(" ", t).strip()
    return t


def tokenize(text: str) -> List[str]:
    """Tokenize cleaned text. Tries NLTK; falls back to whitespace split."""
    if not text:
        return []
    try:
        from nltk.tokenize import word_tokenize  # type: ignore
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    return [tok for tok in tokens if tok and tok.isalnum() or any(c in tok for c in "+#.")]


def remove_stopwords(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t not in _STOPWORDS and len(t) > 1]


def lemmatize(tokens: List[str]) -> List[str]:
    """Lemmatize using NLTK WordNet if available; otherwise return tokens unchanged."""
    try:
        from nltk.stem import WordNetLemmatizer  # type: ignore
        lemm = WordNetLemmatizer()
        return [lemm.lemmatize(t) for t in tokens]
    except Exception:
        return tokens


def preprocess_pipeline(text: str) -> List[str]:
    """Full pipeline: clean -> tokenize -> stopword removal -> lemmatize."""
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    return tokens
