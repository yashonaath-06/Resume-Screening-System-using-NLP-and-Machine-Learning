# Resume Screening AI

> AI-powered Resume Screening System using **NLP + Machine Learning**.
> Upload resumes, paste a job description, get **ATS scores**, **ranked candidates**,
> **skill-gap analysis**, and **downloadable recruiter reports**.

![tech](https://img.shields.io/badge/backend-FastAPI-009688)
![tech](https://img.shields.io/badge/frontend-Next.js%2014-000)
![tech](https://img.shields.io/badge/ml-spaCy%20%7C%20NLTK%20%7C%20sklearn-blue)
![tech](https://img.shields.io/badge/db-SQLite%20%7C%20PostgreSQL-336791)

---

## 1. What this project does

1. Upload resumes in **PDF / DOCX / TXT**.
2. Extract text and run an **NLP pipeline**:
   clean → tokenize → stopword removal → lemmatize → NER.
3. Extract **skills, education, years of experience, keywords, contact info**.
4. Accept a **job description**, optionally with required skills / min experience / education level.
5. Compute a **0–100 ATS score** combining:
   skill match (40%) · semantic similarity (25%) · keyword coverage (15%) ·
   experience match (10%) · education match (10%).
6. **Rank candidates** per job and surface **skill gaps**.
7. Generate a **recruiter-style report** (JSON + downloadable **PDF**).
8. Visualize everything on a **dashboard** with cards, charts, and dark/light mode.

## 2. Architecture

```
┌────────────────────────┐  HTTP  ┌──────────────────────────────┐  ORM   ┌──────────────────┐
│ Next.js + Tailwind UI  │ ─────▶ │ FastAPI (Python)             │ ─────▶ │ SQLite / Postgres │
│ App Router · shadcn    │        │ Routers / Services           │        │ Resumes, Jobs,    │
│ Recharts dashboards    │        │ ML/NLP Pipeline              │        │ Screenings        │
└─────────▲──────────────┘        │  ├ Parser (pdfplumber/docx)  │        └──────────────────┘
          │  JSON + PDF           │  ├ Preprocess (spaCy/NLTK)   │
          └───────────────────────│  ├ NER + Skill/Keyword ext.  │
                                  │  ├ TF-IDF + cosine matcher   │
                                  │  ├ ATS scoring engine        │
                                  │  └ Ranker + Report (PDF)     │
                                  └──────────────────────────────┘
```

## 3. Folder structure

```
resume-screening-ai/
├── backend/                  FastAPI + ML/NLP pipeline
│   ├── app/
│   │   ├── api/              REST routes (health, jobs, resumes, screen, analytics)
│   │   ├── ml/               Parser, preprocess, NER, skill/keyword/edu/exp,
│   │   │                     matcher, ATS, ranker, report
│   │   ├── data/             skills.txt + education_keywords.txt
│   │   ├── config.py db.py models.py schemas.py main.py
│   ├── tests/                Smoke tests for the pipeline
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 Next.js 14 (App Router, TS, Tailwind, shadcn-style)
│   ├── app/                  /, /dashboard, /upload, /jobs, /jobs/[id],
│   │                         /candidates, /analytics, /reports, /reports/[id]
│   ├── components/           ui/ + dashboard/ + jobs/ + upload/ + candidates/ + reports/
│   ├── lib/                  api client, types, utils
│   ├── package.json tailwind.config.ts tsconfig.json
│   └── Dockerfile
├── samples/                  Demo resumes + job descriptions
├── docs/                     Installation, viva, interview, resume points
├── docker-compose.yml
├── setup.sh
├── Makefile
└── README.md
```

## 4. Tech stack

- **Frontend** — Next.js 14, TypeScript, Tailwind CSS, shadcn-style UI primitives,
  Recharts, next-themes, react-dropzone, sonner, lucide-react.
- **Backend** — FastAPI, Pydantic v2, SQLAlchemy 2, Uvicorn.
- **ML / NLP** — spaCy (`en_core_web_sm`), NLTK (stopwords / wordnet),
  scikit-learn (TF-IDF, cosine similarity), optional `sentence-transformers`
  (`all-MiniLM-L6-v2`), pdfplumber, python-docx, ReportLab.
- **DB** — SQLite by default (zero setup), Postgres via `DATABASE_URL`.

## 5. Quick start

### Option A — One command (Docker)

```bash
cd resume-screening-ai
docker compose up --build
```

- Frontend → http://localhost:3000
- Backend  → http://localhost:8000  (Swagger UI at `/docs`)

### Option B — Local dev

```bash
# 1. install everything
bash setup.sh

# 2. terminal 1: backend
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# 3. terminal 2: frontend
cd frontend && npm run dev
```

Open http://localhost:3000.

### Option C — Makefile shortcuts

```bash
make install     # one-shot setup
make backend     # run FastAPI dev server
make frontend    # run Next.js dev server
make test        # run pytest smoke tests
make docker-up   # full stack via docker compose
```

## 6. Demo workflow (60 seconds)

1. Go to **Upload** → drop the three TXT files in `samples/`.
2. Go to **Jobs** → click **Save job** after pasting `samples/sample_jd_backend.txt`
   (leave the skills field empty — they'll be auto-extracted).
3. Click **Screen all resumes** on the job card.
4. Open the job → see ranked candidates, skill gap, and ATS scores.
5. Click **Report** on any candidate → view radar breakdown and **Download PDF**.

## 7. API reference (selected)

| Method | Path                                  | Description                          |
|--------|---------------------------------------|--------------------------------------|
| GET    | `/api/health`                         | Liveness + version                   |
| POST   | `/api/jobs`                           | Create a job description             |
| GET    | `/api/jobs`                           | List jobs                            |
| POST   | `/api/resumes/upload` (multipart)     | Upload one or more resumes           |
| GET    | `/api/resumes`                        | List resumes                         |
| POST   | `/api/screen/run`                     | Run screening for a job              |
| GET    | `/api/screen/job/{job_id}/ranked`     | Ranked candidates per job            |
| GET    | `/api/screen/{id}/report`             | Full screening report (JSON)         |
| GET    | `/api/screen/{id}/report.pdf`         | Recruiter PDF report                 |
| GET    | `/api/analytics/summary`              | Counts + average ATS                 |
| GET    | `/api/analytics/score-distribution`   | ATS histogram                        |
| GET    | `/api/analytics/top-skills`           | Top skills across resumes            |
| GET    | `/api/analytics/skill-gap/{job_id}`   | Aggregate skill gap per job          |

Open the full interactive spec at **http://localhost:8000/docs** when running.

## 8. Configuration

Backend (`backend/.env`):

```
DATABASE_URL=sqlite:///./storage/app.db
UPLOAD_DIR=./uploads
STORAGE_DIR=./storage
CORS_ORIGINS=http://localhost:3000
USE_SENTENCE_TRANSFORMER=false
SENTENCE_MODEL=all-MiniLM-L6-v2
```

Frontend (`frontend/.env.local`):

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 9. Tests

```bash
cd backend && source .venv/bin/activate
pytest -q
```

The smoke suite verifies preprocessing, skill extraction, keyword extraction,
experience estimation, education extraction, similarity, and the full ATS pipeline.

## 10. Documentation index

- [Installation guide](docs/INSTALLATION.md)
- [Setup guide](docs/SETUP.md)
- [Viva questions](docs/VIVA.md)
- [Interview questions](docs/INTERVIEW.md)
- [Resume project points](docs/RESUME_POINTS.md)

## 11. License

For academic / educational use.
