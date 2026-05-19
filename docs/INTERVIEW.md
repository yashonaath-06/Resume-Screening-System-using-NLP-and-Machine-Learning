# Interview Questions

Talking points for placement interviews where this project comes up.

## NLP & ML

1. **Walk me through your NLP pipeline.**
   Cleaning (lowercasing, URL/email/phone stripping) → tokenization (NLTK)
   → stopword removal → lemmatization (WordNet) → spaCy NER for `PERSON`,
   `ORG`, `GPE` etc. → curated-dictionary skill matching → TF-IDF keyword
   extraction.

2. **Why cosine similarity over Euclidean distance?**
   Cosine ignores magnitude, which matters because TF-IDF vectors are not
   normalized by length. Two resumes can be similar in topic but very
   different in length; cosine handles this naturally.

3. **What is TF-IDF and why use it here?**
   `tf(t, d) * log(N / df(t))`. It boosts tokens that are characteristic of
   a given document. For matching resumes to job descriptions, this surfaces
   role-specific terms (e.g. *kubernetes*) over common ones (e.g. *the team*).

4. **What would you change to use deep learning?**
   Replace the matcher with `sentence-transformers/all-MiniLM-L6-v2`
   embeddings + cosine. The toggle already exists
   (`USE_SENTENCE_TRANSFORMER=true`). For better recall, fine-tune on
   resume/JD pairs.

5. **What are the limits of dictionary-based skill extraction?**
   Misses synonyms (`postgresql` vs `postgres`), spelling variants,
   long-tail skills. Mitigations: synonym list, fuzzy matching (RapidFuzz),
   or an LLM-based extractor.

## System design

6. **Why FastAPI over Flask or Django?**
   Async-first, built-in Pydantic validation, OpenAPI docs out of the box,
   strong typing — and excellent fit for ML-serving microservices.

7. **Why SQLite by default?**
   Zero-config single-file DB ideal for a demo. The project switches to
   Postgres by changing one env var.

8. **How would this handle 10,000 resumes?**
   - Move PDF parsing + NLP to a background worker (Celery or RQ).
   - Switch to Postgres + a vector index (pgvector or FAISS).
   - Cache TF-IDF/embedding vectors per resume; recompute only on update.
   - Paginate API responses.

9. **How do you keep the API stateless?**
   Files live on disk (`uploads/`), data lives in the DB. The FastAPI
   process holds no per-request state, so it can be horizontally scaled.

10. **Security considerations?**
    Validate file extension and size, sanitize filenames (we use UUIDs),
    serve uploads via signed URLs in production, restrict CORS to known
    origins, hash any user PII at rest if storing it long-term.

## Frontend

11. **Why App Router?**
    Native file-based routing, layouts, and Server Components.

12. **Why shadcn-style UI?**
    Owning the components keeps us free of upstream churn while still
    inheriting a Tailwind-driven, accessible design system.

13. **Which charts and why?**
    Recharts: declarative SVG charts that compose nicely with React.
    We use bar charts for ATS distribution / top skills and a radar chart
    for the per-candidate score breakdown.

## Data & evaluation

14. **How would you evaluate the screening quality?**
    - Build a labeled dataset (resume, JD, hire/no-hire).
    - Compute Precision@k, Recall@k, NDCG of the ranking.
    - Compare TF-IDF vs sentence-transformer baselines.
    - A/B-test ATS weight configurations.

15. **What about bias and fairness?**
    Resume screening is a high-risk ML use case. Mitigations include:
    redacting names / colleges / locations before scoring, monitoring
    score distributions across demographic slices, providing recruiter
    overrides, and never using race/gender as features.

16. **How would you productize this?**
    Add auth (NextAuth + JWT), org/multi-tenant scoping, audit logs of
    every screening decision, role-based access control, and a structured
    PII redaction step before persistence.
