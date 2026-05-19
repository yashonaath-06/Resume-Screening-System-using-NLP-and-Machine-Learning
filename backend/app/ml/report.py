"""Build recruiter-style reports (JSON + PDF)."""
from __future__ import annotations

import io
from datetime import datetime
from typing import Any, Dict


def _verdict(ats_score: float) -> str:
    if ats_score >= 80:
        return "Strong Match"
    if ats_score >= 65:
        return "Good Match"
    if ats_score >= 50:
        return "Borderline"
    return "Weak Match"


def build_report(resume, job, ats: Dict[str, Any], similarity: float) -> Dict[str, Any]:
    """Compose the structured report stored on the screening row."""
    return {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "candidate": {
            "name": resume.candidate_name or resume.file_name,
            "email": resume.email,
            "phone": resume.phone,
            "experience_years": resume.experience_years,
            "education": resume.education,
            "skills_count": len(resume.skills or []),
        },
        "job": {
            "title": job.title,
            "company": job.company,
            "min_experience_years": job.min_experience_years,
            "required_skills_count": len(job.required_skills or []),
        },
        "scores": {
            "ats_score": ats["ats_score"],
            "similarity": round(similarity * 100, 2),
            "skill_match": ats["skill_match"],
            "keyword_match": ats["keyword_match"],
            "experience_match": ats["experience_match"],
            "education_match": ats["education_match"],
        },
        "weights": ats.get("weights", {}),
        "matched_skills": ats["matched_skills"],
        "missing_skills": ats["missing_skills"],
        "verdict": _verdict(ats["ats_score"]),
        "recommendations": _recommendations(ats),
    }


def _recommendations(ats: Dict[str, Any]) -> list[str]:
    tips: list[str] = []
    if ats["skill_match"] < 60:
        tips.append("Add more required skills to the resume (focus on the missing-skills list).")
    if ats["keyword_match"] < 50:
        tips.append("Mirror keywords from the job description in your resume.")
    if ats["experience_match"] < 60:
        tips.append("Emphasize the duration and depth of relevant work experience.")
    if ats["education_match"] < 60:
        tips.append("Ensure education credentials meet the job requirement.")
    if not tips:
        tips.append("Resume aligns well with the job description.")
    return tips


def render_pdf(resume, job, screening) -> bytes:
    """Render a downloadable recruiter-style PDF report."""
    try:
        from reportlab.lib import colors  # type: ignore
        from reportlab.lib.pagesizes import A4  # type: ignore
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # type: ignore
        from reportlab.platypus import (  # type: ignore
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        )
    except Exception:
        # Minimal fallback: plain-text "PDF" so endpoint still works.
        return _render_text_fallback(resume, job, screening)

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, title="Screening Report")
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], textColor=colors.HexColor("#0f172a"))
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], textColor=colors.HexColor("#1e293b"))
    body = styles["BodyText"]

    story = []
    story.append(Paragraph("Resume Screening Report", h1))
    story.append(Paragraph(f"Generated: {datetime.utcnow().isoformat()}Z", body))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Candidate", h2))
    story.append(Paragraph(f"<b>Name:</b> {resume.candidate_name or resume.file_name}", body))
    story.append(Paragraph(f"<b>Email:</b> {resume.email or '-'}", body))
    story.append(Paragraph(f"<b>Phone:</b> {resume.phone or '-'}", body))
    story.append(Paragraph(f"<b>Experience:</b> {resume.experience_years} years", body))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Job", h2))
    story.append(Paragraph(f"<b>Title:</b> {job.title}", body))
    story.append(Paragraph(f"<b>Company:</b> {job.company or '-'}", body))
    story.append(Paragraph(f"<b>Min experience:</b> {job.min_experience_years} years", body))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Scores", h2))
    table_data = [
        ["Metric", "Score (%)"],
        ["ATS Score", f"{screening.ats_score:.2f}"],
        ["Similarity", f"{screening.similarity * 100:.2f}"],
        ["Skill match", f"{screening.skill_match:.2f}"],
        ["Keyword match", f"{screening.keyword_match:.2f}"],
        ["Experience match", f"{screening.experience_match:.2f}"],
        ["Education match", f"{screening.education_match:.2f}"],
    ]
    t = Table(table_data, hAlign="LEFT", colWidths=[200, 100])
    t.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ])
    )
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Verdict", h2))
    story.append(Paragraph(_verdict(screening.ats_score), body))
    story.append(Spacer(1, 8))

    if screening.matched_skills:
        story.append(Paragraph("Matched skills", h2))
        story.append(Paragraph(", ".join(screening.matched_skills), body))
        story.append(Spacer(1, 6))
    if screening.missing_skills:
        story.append(Paragraph("Missing skills", h2))
        story.append(Paragraph(", ".join(screening.missing_skills), body))
        story.append(Spacer(1, 6))

    doc.build(story)
    return buf.getvalue()


def _render_text_fallback(resume, job, screening) -> bytes:
    lines = [
        "Resume Screening Report",
        f"Candidate: {resume.candidate_name or resume.file_name}",
        f"Job: {job.title}",
        f"ATS Score: {screening.ats_score:.2f}",
        f"Similarity: {screening.similarity * 100:.2f}",
        f"Skill match: {screening.skill_match:.2f}",
        f"Keyword match: {screening.keyword_match:.2f}",
        f"Experience match: {screening.experience_match:.2f}",
        f"Education match: {screening.education_match:.2f}",
        f"Matched: {', '.join(screening.matched_skills or [])}",
        f"Missing: {', '.join(screening.missing_skills or [])}",
    ]
    return ("\n".join(lines)).encode("utf-8")
