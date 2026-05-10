# CourtFind AI — Architecture

## Overview

CourtFind AI is a two-module intelligent sports platform:

1. **Court Discovery** — A\* informed search over a court graph, ranked by a multi-factor heuristic.
2. **Player Matchmaking** — Random Forest classifier predicting match compatibility from player profile features.

---

## System Diagram

```
Client (React/Next.js)
        │
        ▼
FastAPI Application (app/main.py)
    │           │
    ▼           ▼
/courts      /matchmaking
    │              │
    ▼              ▼
AStarCourtSearch   MatchmakingInference
    │                   │
CourtHeuristic      Preprocessor ──► RF Model
    │
HaversineDistance
```

---

## Module Breakdown

### Court Search (`app/services/court_search/`)

| File | Responsibility |
|------|----------------|
| `astar_engine.py` | Priority queue search, open/closed set management |
| `heuristic.py` | Weighted multi-factor scoring: distance + price + rating |
| `graph_builder.py` | Court adjacency graph by proximity (extensible to multi-hop) |
| `scorer.py` | Standalone scorer for debugging/auditing |
| `validators.py` | Hard filters: sport match, budget cap |

**Why A\*?**
Standard greedy best-first search suffices for single-source ranking, but the A\* framing gives us:
- Open/closed set infrastructure ready for graph traversal extensions
- Externalised, tunable heuristic weights per request
- Natural language for future cost function additions (g(n) = booking fee, travel time, etc.)

### Matchmaking (`app/services/matchmaking/`)

| File | Responsibility |
|------|----------------|
| `dataset_generator.py` | Seeded synthetic player data with realistic label logic |
| `feature_engineering.py` | Derived features: `experience_ratio`, `skill_win_interaction` |
| `preprocessing.py` | Stateful `LabelEncoder` + `MinMaxScaler` pipeline |
| `trainer.py` | RF training with SMOTE class balancing |
| `inference.py` | Lazy-loading singleton for thread-safe inference |
| `evaluator.py` | Post-deployment offline evaluation |

### API (`app/api/`)

FastAPI with full Pydantic validation, typed response models, and domain exception → HTTP status mapping.

| Route | Method | Description |
|-------|--------|-------------|
| `/health` | GET | Health check + model readiness |
| `/courts/search` | POST | A\* court recommendation |
| `/matchmaking/predict` | POST | ML compatibility prediction |

---

## Data Flow

### Court Search

```
CourtSearchQuery (validated)
    → validate_query() → hard filter (sport, budget)
    → CourtHeuristic.evaluate() for each candidate
    → heapq.heappush (min-heap by score)
    → pop top-N → CourtSearchResponse
```

### Matchmaking

```
PlayerMatchQuery (validated)
    → MatchmakingPreprocessor.transform()
        → add_derived_features()
        → LabelEncoder per categorical
        → MinMaxScaler on numericals
    → RF.predict() + predict_proba()
    → MatchPrediction response
```

---

## Production Considerations

- **Stateless API** — no in-process session state; safe for horizontal scaling.
- **Lazy model loading** — inference engine loads artefacts on first request, not at import.
- **Thread safety** — scikit-learn `predict` is GIL-safe for concurrent FastAPI workers.
- **Structured logging** — `structlog` emits JSON in production, human-readable in dev.
- **Docker health check** — polls `/health` every 30s; restarts on failure.
- **SMOTE** — handles class imbalance in training; `class_weight="balanced"` as secondary guard.
