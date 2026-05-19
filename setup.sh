#!/usr/bin/env bash
# One-shot setup script for local development.
# Usage: bash setup.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ">> Setting up backend..."
cd "$ROOT_DIR/backend"
python -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm || true
python -m nltk.downloader punkt stopwords wordnet || true
mkdir -p uploads storage
deactivate

echo ">> Setting up frontend..."
cd "$ROOT_DIR/frontend"
if command -v pnpm >/dev/null 2>&1; then
  pnpm install
else
  npm install
fi

echo ""
echo "Setup complete."
echo "Run backend:  cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo "Run frontend: cd frontend && npm run dev"
