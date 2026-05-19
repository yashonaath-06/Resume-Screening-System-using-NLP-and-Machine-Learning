"""ATS (Applicant Tracking System) scoring engine.

Combines five components into a single 0-100 ATS score:

  - skill_match       (40%) — overlap of required skills found in resume
  - similarity        (25%) — semantic / TF-IDF cosine similarity
  - keyword_match     (15%) — coverage of JD keywords in resume tokens
  - experience_match  (10%) — meets minimum years of experience
  - education_match   (10%) — meets required education level

All component scores are normalized to 0..1 and finally scaled to 0..100.
"""
from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List

from .education import meets_requirement
from .preprocess import preprocess_pipeline

WEIGHTS = {
    "skill_match": 0.40,
    "similarity": 0.25,
    "keyword_match": 0.15,
    "experience_match": 0.10,
    "education_match": 0.10,
}


def _normalize(values: Iterable[str]) -> List[str]:
    out = []
    seen = set()
    for v in values or []:
        if not v:
            continue
        x = re.sub(r"\s+", " ", v.strip().lower())
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def _skill_overlap(resume_skills: List[str], job_skills: List[str]) -> Dict[str, Any]:
    rs = _normalize(resume_skills)
    js = _normalize(job_skills)
    if not js:
        # No required skills => treat as full match if resume has any skills
        return {"score": 1.0 if rs else 0.5, "matched": [], "missing": []}
    rs_set = set(rs)
    matched = [s for s in js if s in rs_set]
    missing = [s for s in js if s not in rs_set]
    score = len(matched) / len(js)
    return {"score": score, "matched": matched, "missing": missing}


def _keyword_coverage(resume_text: str, job_text: str) -> float:
    if not job_text:
        return 0.0
    resume_tokens = set(preprocess_pipeline(resume_text))
    job_tokens = preprocess_pipeline(job_text)
    if not job_tokens:
        return 0.0
    # Use the unique top tokens of the JD as the keyword set.
    job_unique = list(dict.fromkeys(job_tokens))[:60]
    if not job_unique:
        return 0.0
    hits = sum(1 for t in job_unique if t in resume_tokens)
    return hits / len(job_unique)


def _experience_score(resume_years: float, min_years: float) -> float:
    if min_years <= 0:
        return 1.0
    if resume_years <= 0:
        return 0.0
    if resume_years >= min_years:
        # Modest bonus capped at 1.0 for substantial extra experience.
        return min(1.0, 0.85 + 0.15 * min(1.0, (resume_years - min_years) / max(1.0, min_years)))
    return max(0.0, resume_years / min_years) * 0.85


def _education_score(resume_education: List[str], required_level: str) -> float:
    if not required_level:
        return 1.0
    return 1.0 if meets_requirement(resume_education, required_level) else 0.4


def compute_ats(
    *,
    resume_skills: List[str],
    job_skills: List[str],
    resume_text: str,
    job_text: str,
    resume_keywords: List[str],
    resume_experience: float,
    min_experience: float,
    resume_education: List[str],
    required_education: str,
    similarity_score: float,
) -> Dict[str, Any]:
    skill = _skill_overlap(resume_skills, job_skills)
    keyword = _keyword_coverage(resume_text, job_text)
    experience = _experience_score(resume_experience or 0.0, min_experience or 0.0)
    education = _education_score(resume_education, required_education)
    sim = max(0.0, min(1.0, float(similarity_score or 0.0)))

    components = {
        "skill_match": skill["score"],
        "similarity": sim,
        "keyword_match": keyword,
        "experience_match": experience,
        "education_match": education,
    }
    raw = sum(components[k] * w for k, w in WEIGHTS.items())
    ats = round(max(0.0, min(1.0, raw)) * 100.0, 2)

    return {
        "ats_score": ats,
        "similarity": round(sim * 100.0, 2),
        "skill_match": round(skill["score"] * 100.0, 2),
        "keyword_match": round(keyword * 100.0, 2),
        "experience_match": round(experience * 100.0, 2),
        "education_match": round(education * 100.0, 2),
        "matched_skills": skill["matched"],
        "missing_skills": skill["missing"],
        "weights": WEIGHTS,
    }
