"""Job description endpoints."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import JobDescription
from ..schemas import JobCreate, JobOut
from ..ml.skill_extractor import SkillExtractor

router = APIRouter(prefix="/jobs", tags=["jobs"])

_skill_extractor = SkillExtractor()


@router.post("", response_model=JobOut, status_code=201)
def create_job(payload: JobCreate, db: Session = Depends(get_db)) -> JobOut:
    required = payload.required_skills
    if not required:
        # auto-extract required skills from description text
        required = _skill_extractor.extract(payload.description)

    job = JobDescription(
        title=payload.title,
        company=payload.company,
        description=payload.description,
        required_skills=required,
        min_experience_years=payload.min_experience_years,
        education_level=payload.education_level,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=List[JobOut])
def list_jobs(db: Session = Depends(get_db)) -> List[JobOut]:
    return db.query(JobDescription).order_by(JobDescription.created_at.desc()).all()


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)) -> JobOut:
    job = db.get(JobDescription, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{job_id}", status_code=204, response_model=None)
def delete_job(job_id: int, db: Session = Depends(get_db)) -> None:
    job = db.get(JobDescription, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
