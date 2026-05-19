"""Screening endpoints: run ATS scoring, ranking, and report generation."""
from __future__ import annotations

import io
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import JobDescription, Resume, Screening
from ..schemas import (
    RankedCandidate,
    ScreenRequest,
    ScreeningOut,
    ScreeningReport,
    JobOut,
    ResumeOut,
)
from ..ml.ats import compute_ats
from ..ml.matcher import similarity
from ..ml.report import build_report, render_pdf

router = APIRouter(prefix="/screen", tags=["screen"])


def _run_screening(db: Session, job: JobDescription, resume: Resume) -> Screening:
    sim = similarity(resume.cleaned_text or resume.raw_text, job.description)
    ats = compute_ats(
        resume_skills=resume.skills,
        job_skills=job.required_skills,
        resume_text=resume.cleaned_text or resume.raw_text,
        job_text=job.description,
        resume_keywords=resume.keywords,
        resume_experience=resume.experience_years,
        min_experience=job.min_experience_years,
        resume_education=resume.education,
        required_education=job.education_level,
        similarity_score=sim,
    )

    scr = (
        db.query(Screening)
        .filter(Screening.resume_id == resume.id, Screening.job_id == job.id)
        .one_or_none()
    )
    if scr is None:
        scr = Screening(resume_id=resume.id, job_id=job.id)
        db.add(scr)

    scr.similarity = sim
    scr.ats_score = ats["ats_score"]
    scr.skill_match = ats["skill_match"]
    scr.keyword_match = ats["keyword_match"]
    scr.experience_match = ats["experience_match"]
    scr.education_match = ats["education_match"]
    scr.matched_skills = ats["matched_skills"]
    scr.missing_skills = ats["missing_skills"]
    scr.report = build_report(resume, job, ats, sim)
    return scr


@router.post("/run", response_model=List[ScreeningOut])
def run_screening(payload: ScreenRequest, db: Session = Depends(get_db)) -> List[ScreeningOut]:
    job = db.get(JobDescription, payload.job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if payload.resume_ids:
        resumes = db.query(Resume).filter(Resume.id.in_(payload.resume_ids)).all()
    else:
        resumes = db.query(Resume).all()

    if not resumes:
        raise HTTPException(status_code=400, detail="No resumes available to screen")

    results: list[Screening] = []
    for r in resumes:
        results.append(_run_screening(db, job, r))
    db.commit()
    for s in results:
        db.refresh(s)
    return results


@router.get("/job/{job_id}/ranked", response_model=List[RankedCandidate])
def ranked_candidates(job_id: int, db: Session = Depends(get_db)) -> List[RankedCandidate]:
    job = db.get(JobDescription, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    rows = (
        db.query(Screening, Resume)
        .join(Resume, Resume.id == Screening.resume_id)
        .filter(Screening.job_id == job_id)
        .order_by(Screening.ats_score.desc())
        .all()
    )
    out: list[RankedCandidate] = []
    for idx, (s, r) in enumerate(rows, start=1):
        out.append(
            RankedCandidate(
                screening_id=s.id,
                resume_id=r.id,
                candidate_name=r.candidate_name or r.file_name,
                email=r.email,
                ats_score=s.ats_score,
                similarity=s.similarity,
                matched_skills=s.matched_skills,
                missing_skills=s.missing_skills,
                rank=idx,
            )
        )
    return out


@router.get("/{screening_id}/report", response_model=ScreeningReport)
def screening_report(screening_id: int, db: Session = Depends(get_db)) -> ScreeningReport:
    s = db.get(Screening, screening_id)
    if not s:
        raise HTTPException(status_code=404, detail="Screening not found")
    return ScreeningReport(
        screening=ScreeningOut.model_validate(s),
        resume=ResumeOut.model_validate(s.resume),
        job=JobOut.model_validate(s.job),
        report=s.report or {},
    )


@router.get("/{screening_id}/report.pdf")
def screening_report_pdf(screening_id: int, db: Session = Depends(get_db)) -> StreamingResponse:
    s = db.get(Screening, screening_id)
    if not s:
        raise HTTPException(status_code=404, detail="Screening not found")
    pdf_bytes = render_pdf(s.resume, s.job, s)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="screening-{screening_id}.pdf"'
        },
    )
