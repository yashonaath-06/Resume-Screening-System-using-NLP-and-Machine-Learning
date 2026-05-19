# Viva Questions & Model Answers

Compact answers you can use directly during a viva or project demo.

### 1. What problem does this project solve?
Recruiters spend hours manually screening resumes against job descriptions.
This system automates that pipeline: it parses resumes, extracts entities and
skills using NLP, computes a 0–100 ATS score against a job description, ranks
candidates, and produces a downloadable recruiter report.

### 2. What is ATS scoring?
ATS = **Applicant Tracking System**. It is the score most companies use to
filter resumes before a human looks at them. Here, it is a weighted combination
of skill overlap, semantic similarity, keyword coverage, experience match, and
education match.

### 3. Which NLP techniques are used?
- **Tokenization** (NLTK / spaCy)
- **Stopword removal** (NLTK + fallback list)
- **Lemmatization** (WordNet)
- **Named-Entity Recognition** (spaCy `en_core_web_sm`)
- **TF-IDF vectorization** (scikit-learn)
- **Cosine similarity** for semantic match
- Optional **sentence-transformer embeddings** for deeper semantic similarity

### 4. Why TF-IDF + cosine similarity?
TF-IDF rewards tokens that are frequent in a document but rare across a corpus,
which captures the topical signature of a resume or job description.
Cosine similarity is scale-invariant and works on the resulting sparse vectors.
This is fast, interpretable, and runs without GPUs — ideal for a demoable
academic project.

### 5. How is the ATS score computed?
```
ATS = 100 * ( 0.40 * skill_match
            + 0.25 * similarity
            + 0.15 * keyword_match
            + 0.10 * experience_match
            + 0.10 * education_match )
```
Each component is normalized to [0, 1] before weighting.

### 6. How are skills extracted?
Through a curated dictionary at `backend/app/data/skills.txt` (200+ entries),
matched with a single compiled regex using lookarounds so that special
characters like `+`, `#`, `.` work correctly (e.g. `c++`, `c#`, `node.js`).

### 7. How is years of experience extracted?
Two strategies, then take the max:
1. Explicit phrases like *"6 years of experience"*.
2. Sum of non-overlapping employment date ranges parsed from the text
   (e.g. `Jan 2020 - Present`).

### 8. How does the report PDF work?
Generated server-side with **ReportLab**: candidate info, ATS table, verdict,
matched/missing skills, recommendations. Streamed via FastAPI as
`application/pdf`.

### 9. Why FastAPI?
Async-friendly, great Pydantic v2 integration, automatic Swagger UI, and
high throughput with uvicorn. Perfect for an ML-serving REST API.

### 10. Why Next.js + Tailwind + shadcn-style UI?
- App Router gives us file-based routing and Server Components.
- Tailwind keeps styling consistent and fast to write.
- shadcn-style primitives (button, card, badge, etc.) deliver an
  industry-grade look without external CLI dependencies.

### 11. How does the system rank candidates?
For a given job, we order all `Screening` rows by `ats_score DESC`. The
top of the list is what the dashboard shows; the API returns rank,
matched/missing skills, and email per candidate.

### 12. How do you handle PDF / DOCX parsing?
- `pdfplumber` for PDFs (extracts text per page).
- `python-docx` for DOCX (reads paragraphs).
- TXT is read directly. Each parser fails gracefully and returns an empty
  string so the rest of the pipeline keeps working.

### 13. What is skill-gap analysis?
For each screening, the JD's required skills minus the resume's skills give
the candidate's missing skills. Aggregating over all candidates per job tells
the recruiter which skills are systematically lacking — useful for upskilling
plans and JD adjustments.

### 14. How is the database modeled?
Three tables: `resumes`, `job_descriptions`, `screenings` (FK to both).
JSON columns store skills, education, keywords, entities, and the full
report payload — keeping the schema simple while preserving rich data.

### 15. Can it scale?
For demo: SQLite is fine. For production: switch `DATABASE_URL` to Postgres,
run uvicorn with multiple workers behind nginx, and mount `uploads/` and
`storage/` on persistent volumes. Sentence-transformer inference can be
moved to a worker queue if needed.
