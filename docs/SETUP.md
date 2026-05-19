# Setup Guide

A more detailed walkthrough — useful if you want to extend or grade the project.

## 1. Repository layout

```
resume-screening-ai/
├── backend/        FastAPI + ML pipeline
├── frontend/       Next.js dashboard
├── samples/        Demo resumes + job descriptions
├── docs/           Documentation
├── docker-compose.yml
├── setup.sh
└── Makefile
```

## 2. Environment variables

### Backend (`backend/.env`)

| Variable                   | Default                              | Notes                                    |
|----------------------------|--------------------------------------|------------------------------------------|
| `DATABASE_URL`             | `sqlite:///./storage/app.db`         | Use `postgresql+psycopg2://...` for PG   |
| `UPLOAD_DIR`               | `./uploads`                          | Where uploaded files are stored          |
| `STORAGE_DIR`              | `./storage`                          | DB + cache files                         |
| `CORS_ORIGINS`             | `http://localhost:3000`              | Comma-separated list                     |
| `USE_SENTENCE_TRANSFORMER` | `false`                              | Set `true` to enable semantic similarity |
| `SENTENCE_MODEL`           | `all-MiniLM-L6-v2`                   | Any sentence-transformers model          |

### Frontend (`frontend/.env.local`)

| Variable               | Default                  | Notes                  |
|------------------------|--------------------------|------------------------|
| `NEXT_PUBLIC_API_URL`  | `http://localhost:8000`  | Backend base URL       |

## 3. Database

By default the app uses **SQLite** (zero setup). To use **PostgreSQL**:

```bash
# 1. Provision a Postgres database (locally, or with docker run postgres)
# 2. Set DATABASE_URL in backend/.env, e.g.:
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/resume_ai
# 3. Add psycopg2-binary to backend/requirements.txt and reinstall.
# 4. Restart the API; tables are created automatically on startup.
```

## 4. ML model choices

- **Default**: `TfidfVectorizer` + cosine similarity (sklearn).
  Fast, deterministic, no GPU, no model downloads at runtime — ideal for academic demos.
- **Optional**: `sentence-transformers` for semantic similarity. Set
  `USE_SENTENCE_TRANSFORMER=true` and (optionally) change `SENTENCE_MODEL`.
  The first request loads the model into memory.

## 5. Skills corpus

`backend/app/data/skills.txt` contains 200+ curated skills. Add or remove lines —
no rebuild needed; the corpus is reloaded on app start. Multi-word skills
(e.g. `machine learning`) are matched as phrases.

## 6. ATS weights

Defined in `backend/app/ml/ats.py`:

```python
WEIGHTS = {
    "skill_match":      0.40,
    "similarity":       0.25,
    "keyword_match":    0.15,
    "experience_match": 0.10,
    "education_match":  0.10,
}
```

Tweak these to match your hiring philosophy. The five components always
sum to 1.0 so the final score remains in 0..100.

## 7. Adding new endpoints

1. Add a router file in `backend/app/api/`.
2. Register it in `backend/app/main.py` via `app.include_router(...)`.
3. Add a typed wrapper in `frontend/lib/api.ts`.
4. Use it from a page or component.

## 8. Production notes

- Run `uvicorn app.main:app --workers 4` behind a reverse proxy (nginx / Caddy).
- Mount `backend/uploads` and `backend/storage` on persistent volumes.
- Switch to Postgres for concurrent writes.
- Cache the sentence-transformer model into the Docker image to avoid cold starts.
