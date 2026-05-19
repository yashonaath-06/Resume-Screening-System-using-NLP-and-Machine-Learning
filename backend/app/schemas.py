"""Pydantic schemas for API request/response payloads."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ---------- Job descriptions ----------

class JobCreate(BaseModel):
    title: str
    company: str = ""
    description: str
    required_skills: List[str] = Field(default_factory=list)
    min_experience_years: float = 0.0
    education_level: str = ""


class JobOut(BaseModel):
    id: int
    title: str
    company: str
    description: str
    required_skills: List[str]
    min_experience_years: float
    education_level: str
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Resumes ----------

class ResumeOut(BaseModel):
    id: int
    candidate_name: str
    email: str
    phone: str
    file_name: str
    file_type: str
    skills: List[str]
    education: List[str]
    experience_years: float
    keywords: List[str]
    entities: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Screenings ----------

class ScreenRequest(BaseModel):
    job_id: int
    resume_ids: Optional[List[int]] = None  # None => screen against all resumes


class ScreeningOut(BaseModel):
    id: int
    resume_id: int
    job_id: int
    ats_score: float
    similarity: float
    skill_match: float
    keyword_match: float
    experience_match: float
    education_match: float
    matched_skills: List[str]
    missing_skills: List[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RankedCandidate(BaseModel):
    screening_id: int
    resume_id: int
    candidate_name: str
    email: str
    ats_score: float
    similarity: float
    matched_skills: List[str]
    missing_skills: List[str]
    rank: int


class ScreeningReport(BaseModel):
    screening: ScreeningOut
    resume: ResumeOut
    job: JobOut
    report: Dict[str, Any]


# ---------- Misc ----------

class HealthOut(BaseModel):
    status: str
    version: str
