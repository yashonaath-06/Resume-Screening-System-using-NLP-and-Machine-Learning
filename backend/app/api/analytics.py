"""Analytics endpoints: aggregate stats for the dashboard."""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import JobDescription, Resume, Screening

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def summary(db: Session = Depends(get_db)) -> Dict[str, Any]:
    n_resumes = db.query(Resume).count()
    n_jobs = db.query(JobDescription).count()
    n_screenings = db.query(Screening).count()
    avg_ats = 0.0
    if n_screenings > 0:
        avg_ats = (
            db.query(Screening).with_entities(Screening.ats_score).all()
        )
        scores = [s[0] for s in avg_ats]
        avg_ats = round(sum(scores) / len(scores), 2) if scores else 0.0
    return {
        "resumes": n_resumes,
        "jobs": n_jobs,
        "screenings": n_screenings,
        "avg_ats_score": avg_ats,
    }


@router.get("/score-distribution")
def score_distribution(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Return ATS-score histogram in 10-point buckets."""
    buckets = [0] * 10
    scores = [s.ats_score for s in db.query(Screening).all()]
    for s in scores:
        idx = min(int(s // 10), 9)
        buckets[idx] += 1
    return [{"bucket": f"{i*10}-{i*10+9}", "count": c} for i, c in enumerate(buckets)]


@router.get("/top-skills")
def top_skills(limit: int = 15, db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    counter: Counter[str] = Counter()
    for r in db.query(Resume).all():
        for s in r.skills or []:
            counter[s] += 1
    return [{"skill": k, "count": v} for k, v in counter.most_common(limit)]


@router.get("/skill-gap/{job_id}")
def skill_gap(job_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Aggregate which required skills are most often missing across screenings."""
    job = db.get(JobDescription, job_id)
    if not job:
        return {"job_id": job_id, "gaps": []}
    counter: Counter[str] = Counter()
    total = 0
    for s in db.query(Screening).filter(Screening.job_id == job_id).all():
        total += 1
        for ms in s.missing_skills or []:
            counter[ms] += 1
    gaps = [{"skill": k, "candidates_missing": v} for k, v in counter.most_common(20)]
    return {"job_id": job_id, "total_screenings": total, "gaps": gaps}
