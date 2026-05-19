"""Cosine-similarity matcher between resume and job description.

By default uses TF-IDF (sklearn). If USE_SENTENCE_TRANSFORMER=true and the
sentence-transformers library is available, uses a sentence-transformer
model for semantic similarity instead.
"""
from __future__ import annotations

import logging
import math
from typing import Iterable

from ..config import get_settings

logger = logging.getLogger(__name__)
_settings = get_settings()

_st_model = None


def _get_st_model():
    global _st_model
    if _st_model is not None:
        return _st_model
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
        _st_model = SentenceTransformer(_settings.sentence_model)
    except Exception as e:
        logger.warning("Sentence transformer unavailable: %s", e)
        _st_model = False
    return _st_model


def _cosine(a: Iterable[float], b: Iterable[float]) -> float:
    a = list(a)
    b = list(b)
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def _tfidf_similarity(text_a: str, text_b: str) -> float:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
        from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
        vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=5000)
        m = vec.fit_transform([text_a or "", text_b or ""])
        sim = float(cosine_similarity(m[0], m[1])[0, 0])
        return max(0.0, min(1.0, sim))
    except Exception as e:
        logger.warning("TF-IDF similarity failed: %s", e)
        # Final fallback: jaccard over tokens.
        a = set((text_a or "").lower().split())
        b = set((text_b or "").lower().split())
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b)


def _semantic_similarity(text_a: str, text_b: str) -> float:
    model = _get_st_model()
    if not model:
        return _tfidf_similarity(text_a, text_b)
    try:
        emb = model.encode([text_a or " ", text_b or " "], normalize_embeddings=True)
        return float(_cosine(emb[0], emb[1]))
    except Exception as e:
        logger.warning("Semantic similarity failed: %s", e)
        return _tfidf_similarity(text_a, text_b)


def similarity(resume_text: str, job_text: str) -> float:
    if _settings.use_sentence_transformer:
        return _semantic_similarity(resume_text, job_text)
    return _tfidf_similarity(resume_text, job_text)
