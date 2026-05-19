"""Resume endpoints: upload, list, get, delete."""
from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..config import get_settings
from ..db import get_db
from ..models import Resume
from ..schemas import ResumeOut
from ..ml.parser import parse_resume_file
from ..ml.preprocess import clean_text
from ..ml.ner import extract_entities, guess_name_email_phone
from ..ml.skill_extractor import SkillExtractor
from ..ml.keyword_extractor import extract_keywords
from ..ml.experience import estimate_experience_years
from ..ml.education import extract_education

router = APIRouter(prefix="/resumes", tags=["resumes"])
settings = get_settings()
_skill_extractor = SkillExtractor()

ALLOWED_EXT = {".pdf", ".docx", ".txt"}


def _save_upload(file: UploadFile) -> tuple[str, str, str]:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    safe_name = f"{uuid.uuid4().hex}{ext}"
    dest = Path(settings.upload_dir) / safe_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("wb") as f:
        f.write(file.file.read())
    return file.filename or safe_name, str(dest), ext.lstrip(".")


@router.post("/upload", response_model=List[ResumeOut], status_code=201)
def upload_resumes(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
) -> List[ResumeOut]:
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    out: list[Resume] = []
    for f in files:
        original_name, path, ext = _save_upload(f)
        raw = parse_resume_file(path, ext)
        cleaned = clean_text(raw)

        ents = extract_entities(raw)
        contact = guess_name_email_phone(raw, ents)
        skills = _skill_extractor.extract(raw)
        keywords = extract_keywords(cleaned, top_k=25)
        years = estimate_experience_years(raw)
        education = extract_education(raw)

        resume = Resume(
            candidate_name=contact["name"],
            email=contact["email"],
            phone=contact["phone"],
            file_name=original_name,
            file_path=path,
            file_type=ext,
            raw_text=raw,
            cleaned_text=cleaned,
            skills=skills,
            education=education,
            experience_years=years,
            keywords=keywords,
            entities=ents,
        )
        db.add(resume)
        out.append(resume)

    db.commit()
    for r in out:
        db.refresh(r)
    return out


@router.get("", response_model=List[ResumeOut])
def list_resumes(db: Session = Depends(get_db)) -> List[ResumeOut]:
    return db.query(Resume).order_by(Resume.created_at.desc()).all()


@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume(resume_id: int, db: Session = Depends(get_db)) -> ResumeOut:
    r = db.get(Resume, resume_id)
    if not r:
        raise HTTPException(status_code=404, detail="Resume not found")
    return r


@router.delete("/{resume_id}", status_code=204, response_model=None)
def delete_resume(resume_id: int, db: Session = Depends(get_db)) -> None:
    r = db.get(Resume, resume_id)
    if not r:
        raise HTTPException(status_code=404, detail="Resume not found")
    try:
        if r.file_path and os.path.exists(r.file_path):
            os.remove(r.file_path)
    except OSError:
        pass
    db.delete(r)
    db.commit()
