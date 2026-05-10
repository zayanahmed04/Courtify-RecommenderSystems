# CourtFind AI — Agile Sprint Plan

## Sprint 1 — Project Foundation
**Goal:** Establish repository structure, configuration, and core contracts.

### Deliverables
- Full directory scaffold (`app/`, `tests/`, `docs/`, `scripts/`, `frontend/`)
- `requirements.txt` with pinned versions
- `app/config.py` — pydantic-settings environment config
- `app/logging_config.py` — structlog structured logging
- `app/core/constants.py` — system-wide constants
- `app/core/exceptions.py` — domain exception hierarchy
- `app/models/court.py` — Court + CourtSearchQuery Pydantic models
- `app/models/player.py` — Player + PlayerMatchQuery Pydantic models
- `app/models/response_models.py` — typed API response models
- `.env.example`, `.gitignore`, `pytest.ini`, `pyproject.toml`

### Definition of Done
- All models import without errors
- Constants and exceptions are importable from core
- Config reads from `.env` with sensible defaults

---

## Sprint 2 — A* Court Search Engine
**Goal:** Build and validate the A* informed search system.

### Deliverables
- `app/services/shared/distance.py` — Haversine formula
- `app/services/shared/metrics.py` — normalize, clamp, weighted_sum
- `app/services/court_search/heuristic.py` — HeuristicWeights + CourtHeuristic
- `app/services/court_search/graph_builder.py` — proximity graph
- `app/services/court_search/astar_engine.py` — priority queue search
- `app/services/court_search/scorer.py` — standalone court scorer
- `app/services/court_search/validators.py` — hard query filters

### Definition of Done
- A* returns sorted results (ascending score)
- Hard filters eliminate out-of-sport and over-budget courts
- `NoCourtsFoundError` raised cleanly when no candidates exist
- Heuristic weights validated to sum to 1.0

---

## Sprint 3 — Matchmaking Data & Feature Pipeline
**Goal:** Generate training data and build the preprocessing pipeline.

### Deliverables
- `app/services/matchmaking/dataset_generator.py` — seeded synthetic data
- `app/services/matchmaking/feature_engineering.py` — derived features
- `app/services/matchmaking/preprocessing.py` — stateful encode + scale pipeline

### Definition of Done
- Dataset generates 1000 balanced records reproducibly
- All three compatibility classes (Low/Mid/High) present
- Preprocessor fits on training data, serialises to disk, transforms correctly at inference

---

## Sprint 4 — ML Training, Evaluation & Inference
**Goal:** Train the Random Forest model and expose a production-ready inference engine.

### Deliverables
- `app/services/matchmaking/trainer.py` — SMOTE + RF training pipeline
- `app/services/matchmaking/evaluator.py` — offline evaluation
- `app/services/matchmaking/inference.py` — lazy-loading singleton

### Definition of Done
- Model achieves ≥ 75% accuracy on held-out test set
- SMOTE applied before training to handle class imbalance
- Inference engine raises `ModelNotTrainedError` cleanly before artefacts exist
- Model artefacts serialised to `data/models/`

---

## Sprint 5 — API Integration, Frontend & Docker
**Goal:** Wire all services into a production FastAPI application with Docker support.

### Deliverables
- `app/api/dependencies.py` — DI: inference engine, courts, search engine
- `app/api/routes/health.py`, `courts.py`, `matchmaking.py`
- `app/main.py` — FastAPI app with CORS, global exception handler
- `Dockerfile` — multi-stage, non-root user, HEALTHCHECK
- `docker-compose.yml` — API service + optional trainer profile
- `Makefile` — developer productivity targets
- `frontend/` — Next.js + TypeScript frontend scaffold
- `frontend/services/api.ts` — typed API client

### Definition of Done
- All three routes respond correctly via `TestClient`
- 422 on invalid payloads, 404/503 on domain errors
- Docker build succeeds and health check passes
- CORS configured for frontend origin

---

## Sprint 6 — Tests, Scripts, Benchmarks & Documentation
**Goal:** Complete the testing suite, developer tooling, and all documentation.

### Deliverables
- `tests/test_astar.py` — A* unit + edge case tests
- `tests/test_heuristic.py` — heuristic + Haversine + metrics tests
- `tests/test_matchmaking.py` — dataset, feature engineering, preprocessor tests
- `tests/test_api.py` — FastAPI integration tests
- `tests/test_performance.py` — A* latency benchmarks
- `scripts/generate_data.py` — data generation script
- `scripts/train_model.py` — training pipeline script
- `scripts/seed_courts.py` — court seed data script
- `scripts/benchmark_astar.py` — CLI performance benchmark table
- `app/cli/demo.py` — rich CLI demo
- `app/utils/visualization.py` — matplotlib/seaborn plots
- `docs/architecture.md`, `docs/api_contracts.md`, `docs/deployment.md`

### Definition of Done
- All unit tests pass
- API tests pass (503 expected for matchmaking without trained model)
- A* completes in < 500ms for 5000 courts
- Benchmark script outputs latency table
- All docs rendered and accurate

---

## Velocity Summary

| Sprint | Duration | Story Points | Status |
|--------|----------|--------------|--------|
| 1 | 2 days | 13 | ✅ Complete |
| 2 | 3 days | 21 | ✅ Complete |
| 3 | 2 days | 13 | ✅ Complete |
| 4 | 3 days | 21 | ✅ Complete |
| 5 | 3 days | 21 | ✅ Complete |
| 6 | 3 days | 21 | ✅ Complete |
| **Total** | **16 days** | **110** | ✅ |
