SHELL := /bin/bash

.PHONY: help install backend frontend dev docker-up docker-down test clean

help:
	@echo "Targets:"
	@echo "  install      - install backend + frontend dependencies"
	@echo "  backend      - run FastAPI dev server (port 8000)"
	@echo "  frontend     - run Next.js dev server (port 3000)"
	@echo "  test         - run backend pytest suite"
	@echo "  docker-up    - start full stack via docker-compose"
	@echo "  docker-down  - stop docker-compose stack"
	@echo "  clean        - remove caches, build artifacts, db, uploads"

install:
	bash setup.sh

backend:
	cd backend && \
	  source .venv/bin/activate && \
	  uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

test:
	cd backend && \
	  source .venv/bin/activate && \
	  pytest -q

docker-up:
	docker compose up --build

docker-down:
	docker compose down

clean:
	rm -rf backend/.venv backend/__pycache__ backend/storage backend/uploads backend/.pytest_cache
	rm -rf frontend/node_modules frontend/.next
