# CourtFind AI

> Production-grade AI system for intelligent sports court discovery and player matchmaking.

---

## Features

| Module | Technology | Description |
|--------|-----------|-------------|
| Court Discovery | A\* Search | Multi-factor heuristic: distance + price + rating |
| Player Matchmaking | Random Forest | Skill, style, experience → Low / Mid / High compatibility |
| REST API | FastAPI | Typed endpoints, Pydantic validation, structured error responses |
| Data Pipeline | scikit-learn + SMOTE | Synthetic data generation, preprocessing, training, evaluation |
| Logging | structlog | JSON in production, human-readable in development |
| Deployment | Docker + Vercel | Containerised API, standalone Next.js frontend |
| Testing | pytest | Unit, integration, and performance benchmarks |

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate training data + train the model
make full-setup

# 3. Start the API
make run

# 4. Open interactive docs
open http://localhost:8000/docs
```

Or with Docker:

```bash
docker-compose --profile train run trainer   # Train model
docker-compose up                            # Start API
```

---

## Project Structure

```
courtfind-ai/
├── app/
│   ├── api/routes/          # FastAPI route handlers
│   ├── core/                # Constants, exceptions
│   ├── models/              # Pydantic request/response models
│   ├── services/
│   │   ├── court_search/    # A* engine, heuristic, graph, validators
│   │   ├── matchmaking/     # Dataset, preprocessing, training, inference
│   │   └── shared/          # Distance, metrics, serialization
│   ├── utils/               # Visualization, file utils, seed
│   └── cli/                 # Rich CLI demo
├── scripts/                 # Data generation, training, benchmarks
├── tests/                   # pytest test suite
├── frontend/                # Next.js + TypeScript frontend
├── docs/                    # Architecture, API contracts, deployment
├── data/
│   ├── raw/                 # Source court CSV
│   ├── processed/           # Training dataset
│   └── models/              # Serialised ML artefacts
├── Dockerfile
├── docker-compose.yml
└── Makefile
```

---

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Health check + model readiness |
| POST | `/courts/search` | A\* court recommendation |
| POST | `/matchmaking/predict` | ML match compatibility prediction |

See [`docs/api_contracts.md`](docs/api_contracts.md) for full request/response schemas.

---

## Example Requests

### Court Search
```bash
curl -X POST http://localhost:8000/courts/search \
  -H "Content-Type: application/json" \
  -d '{
    "sport": "Padel",
    "budget": 1500,
    "location": [24.8607, 67.0011],
    "max_results": 3
  }'
```

### Matchmaking Prediction
```bash
curl -X POST http://localhost:8000/matchmaking/predict \
  -H "Content-Type: application/json" \
  -d '{
    "skill_level": 7,
    "preferred_sport": "Padel",
    "play_style": "Balanced",
    "availability_hours": 10,
    "avg_session_duration": 90,
    "win_rate": 0.75,
    "age_group": "Young Adult",
    "location_zone": "South",
    "games_played": 120
  }'
```

---

## Running Tests

```bash
# Full test suite
pytest

# With coverage
pytest --cov=app

# Performance benchmarks only
pytest tests/test_performance.py -v -s

# Standalone A* benchmark table
python scripts/benchmark_astar.py
```

---

## CLI Demo

```bash
python -m app.cli.demo
```

Runs both the A\* court search and the matchmaking prediction (requires trained model) in a rich terminal UI.

---

## Tech Stack

**Backend:** Python 3.11, FastAPI, scikit-learn, imbalanced-learn, pandas, numpy, joblib, structlog

**Frontend:** Next.js 14, TypeScript, Tailwind CSS

**Deployment:** Docker, docker-compose, Vercel

---

## Supported Sports

Cricket · Football · Padel · Badminton · Basketball

## Supported Zones (Karachi)

North · South · Central · East · West

---

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for a full system diagram and module breakdown.

## Deployment

See [`docs/deployment.md`](docs/deployment.md) for local, Docker, and Vercel deployment steps.

## Agile Sprints

See [`docs/agile_sprints.md`](docs/agile_sprints.md) for the full 6-sprint delivery plan.
