# Installation Guide

## Prerequisites

- **Python 3.10+** (3.11 recommended)
- **Node.js 18+** (20 recommended)
- **Git**
- Optional: **Docker** & **Docker Compose** for one-command setup

## Option A — Docker (recommended for the demo)

```bash
git clone <your-fork-url>.git
cd <repo>/resume-screening-ai
docker compose up --build
```

Open http://localhost:3000.

## Option B — Local install (no Docker)

### 1. Backend

```bash
cd resume-screening-ai/backend
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Download NLP resources (one-time)
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords wordnet

# Start API
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

In a new terminal:

```bash
cd resume-screening-ai/frontend
npm install                         # or pnpm install / yarn
cp .env.example .env.local          # adjust if backend is not on localhost:8000
npm run dev
```

Open http://localhost:3000.

## Option C — Makefile

```bash
cd resume-screening-ai
make install     # installs both backend and frontend
make backend     # run FastAPI
make frontend    # run Next.js (in another terminal)
make test        # run backend smoke tests
```

## Troubleshooting

### `spaCy model not found`
Run `python -m spacy download en_core_web_sm` inside the backend `venv`.
The app will still start with a blank pipeline if download fails — NER will
just return an empty result.

### `nltk_data` missing
Run `python -m nltk.downloader punkt stopwords wordnet`.
The preprocessor falls back to a built-in stopword list and whitespace
tokenization if NLTK data is unavailable.

### CORS error from the frontend
Make sure `CORS_ORIGINS` in `backend/.env` matches your frontend origin
(e.g. `http://localhost:3000`).

### Resume upload fails with HTTP 400
Only `.pdf`, `.docx`, and `.txt` are accepted. Scanned PDFs without text
require OCR (out of scope for this project).
