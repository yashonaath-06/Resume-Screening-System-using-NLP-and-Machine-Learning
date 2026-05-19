# Resume Project Points

Bullet points you can drop directly onto your CV.

## Short version (3 bullets)

- Built a full-stack **AI Resume Screening System** (Next.js + FastAPI + scikit-learn + spaCy)
  that parses resumes, extracts skills/experience/education with NLP, and ranks candidates
  against a job description using a weighted **ATS scoring engine**.
- Designed a 5-component ATS score (skill match, TF-IDF cosine similarity, keyword
  coverage, experience, education) and surfaced **skill-gap analytics** with
  Recharts dashboards.
- Generated **recruiter-style PDF reports** with ReportLab, exposed a typed REST
  API over FastAPI, and shipped a Dockerized deployment with SQLite/Postgres
  support.

## Long version (resume bullets)

- **Resume Screening AI** — Full-stack project to automate resume screening and
  ATS scoring for recruiters.
  - Implemented an NLP pipeline (spaCy NER, NLTK tokenization/lemmatization,
    TF-IDF keyword extraction) that parses **PDF / DOCX / TXT** resumes and
    extracts skills (200+ curated corpus), experience (regex + date-range
    arithmetic), education levels, and contact info.
  - Designed a weighted **ATS scoring engine** combining skill overlap (40%),
    TF-IDF cosine similarity (25%), keyword coverage (15%), experience match
    (10%), and education match (10%); optional `sentence-transformers`
    embeddings can be enabled with one env var.
  - Built a **FastAPI** backend with Pydantic v2 schemas, SQLAlchemy 2 models,
    and routes for resumes, jobs, screenings, analytics, and report PDFs
    (ReportLab); auto-generated Swagger UI at `/docs`.
  - Built a **Next.js 14** App Router frontend with TypeScript, Tailwind CSS,
    shadcn-style primitives, dark/light theming, drag-and-drop uploads
    (react-dropzone), and Recharts dashboards (score distribution, top skills,
    radar breakdown).
  - Containerized the system with **Docker Compose**, added a Makefile for
    one-shot install, smoke tests via pytest, and seed sample data so the
    system runs end-to-end out of the box.

## Project metrics to mention

- **15+ REST endpoints** documented via OpenAPI/Swagger UI.
- **5-component ATS score** with adjustable weights.
- **200+ skills** in the curated corpus; multi-word phrases supported (`machine learning`, `node.js`).
- **3 file formats** (PDF, DOCX, TXT) parsed end-to-end.
- **PDF + JSON** screening reports.
- **Dark/light themes**, responsive layout, accessible UI primitives.

## Talking points for the recruiter

- Separation of concerns: ML logic lives in `app/ml/` so it can be unit-tested
  and reused outside FastAPI.
- Graceful degradation: every NLP step has a fallback so the system runs even
  if `spaCy`, NLTK, or `sentence-transformers` is unavailable.
- The frontend is fully decoupled — a typed API client (`lib/api.ts`) is the
  only contract between layers.
