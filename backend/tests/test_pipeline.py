"""Smoke tests for the ML/NLP pipeline."""
from __future__ import annotations

from app.ml.preprocess import clean_text, preprocess_pipeline
from app.ml.skill_extractor import SkillExtractor
from app.ml.keyword_extractor import extract_keywords
from app.ml.experience import estimate_experience_years
from app.ml.education import extract_education, highest_level
from app.ml.matcher import similarity
from app.ml.ats import compute_ats


SAMPLE_RESUME = """
John Doe
john.doe@example.com  +1 (555) 123-4567

Summary
Senior backend engineer with 6 years of experience building Python services
on AWS. Strong in FastAPI, Django, PostgreSQL, Docker, and Kubernetes.

Experience
Acme Corp - Senior Engineer (Jan 2020 - Present)
  Built microservices in Python and Go on Kubernetes.
Globex - Engineer (Jun 2017 - Dec 2019)
  REST APIs in Django and PostgreSQL.

Education
B.Tech in Computer Science, 2017
"""

SAMPLE_JD = """
We are hiring a Senior Backend Engineer with 5+ years of experience.
Required skills: Python, FastAPI, PostgreSQL, Docker, Kubernetes, AWS.
Bachelor's degree in CS or equivalent required.
"""


def test_clean_and_preprocess():
    cleaned = clean_text(SAMPLE_RESUME)
    assert "john.doe" not in cleaned  # email stripped
    tokens = preprocess_pipeline(SAMPLE_RESUME)
    assert "python" in tokens
    assert "fastapi" in tokens or "fastapi" in cleaned


def test_skill_extraction():
    sk = SkillExtractor()
    skills = sk.extract(SAMPLE_RESUME)
    assert "python" in skills
    assert "fastapi" in skills
    assert "kubernetes" in skills


def test_keyword_extraction():
    kws = extract_keywords(SAMPLE_RESUME, top_k=10)
    assert isinstance(kws, list) and len(kws) > 0


def test_experience_estimation():
    yrs = estimate_experience_years(SAMPLE_RESUME)
    assert yrs >= 5.0


def test_education_extraction():
    found = extract_education(SAMPLE_RESUME)
    assert any("b.tech" in f or "bachelor" in f for f in found)
    assert highest_level(found) in {"bachelors", "masters", "phd"}


def test_similarity_and_ats():
    sim = similarity(SAMPLE_RESUME, SAMPLE_JD)
    assert 0.0 <= sim <= 1.0

    ats = compute_ats(
        resume_skills=["python", "fastapi", "postgresql", "docker", "kubernetes", "aws"],
        job_skills=["python", "fastapi", "postgresql", "docker", "kubernetes", "aws"],
        resume_text=SAMPLE_RESUME,
        job_text=SAMPLE_JD,
        resume_keywords=[],
        resume_experience=6.0,
        min_experience=5.0,
        resume_education=["b.tech", "bachelor"],
        required_education="bachelors",
        similarity_score=sim,
    )
    assert ats["ats_score"] >= 70
    assert "python" in ats["matched_skills"]
    assert ats["missing_skills"] == []
