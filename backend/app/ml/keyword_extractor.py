"""Keyword extraction using TF-IDF; falls back to frequency-based extraction."""
from __future__ import annotations

from collections import Counter
from typing import List

from .preprocess import preprocess_pipeline


def extract_keywords(text: str, top_k: int = 25) -> List[str]:
    if not text:
        return []
    tokens = preprocess_pipeline(text)
    if not tokens:
        return []

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
        # Rebuild a single-document corpus; feed sentence-like splits to get IDF.
        sentences = [s for s in text.split(".") if s.strip()]
        if len(sentences) < 2:
            sentences = [" ".join(tokens[i:i + 10]) for i in range(0, len(tokens), 10)] or [" ".join(tokens)]
        vec = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 2),
            stop_words="english",
            lowercase=True,
        )
        matrix = vec.fit_transform(sentences)
        # Aggregate scores across sentences.
        scores = matrix.sum(axis=0).A1
        terms = vec.get_feature_names_out()
        ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
        return [t for t, _ in ranked[:top_k]]
    except Exception:
        # Fallback: top-frequency tokens
        counts = Counter(tokens)
        return [w for w, _ in counts.most_common(top_k)]
