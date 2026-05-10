# CourtFind AI — Deployment Guide

## Local Development

```bash
# 1. Clone and install
git clone <repo>
cd courtfind-ai
pip install -r requirements.txt

# 2. Generate training data
python scripts/generate_data.py

# 3. Train the model
python scripts/train_model.py

# 4. Start the API
uvicorn app.main:app --reload

# 5. (Optional) Run the CLI demo
python -m app.cli.demo

# One-shot with Makefile
make full-setup && make run
```

---

## Docker

```bash
# Build
docker build -t courtfind-ai:latest .

# Run API
docker-compose up

# Run training only
docker-compose --profile train run trainer

# Full workflow
docker-compose --profile train run trainer && docker-compose up api
```

Model artefacts in `data/` are mounted as a volume, so they persist between container restarts.

---

## Frontend

```bash
cd frontend
npm install
npm run dev        # http://localhost:3000
npm run build      # Production build
```

Set `NEXT_PUBLIC_API_URL` env var for non-local API endpoints.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | CourtFind AI | Service name shown in health check |
| `DEBUG` | true | Enables human-readable logs |
| `LOG_LEVEL` | INFO | DEBUG / INFO / WARNING / ERROR |
| `MODEL_PATH` | data/models/matcher_model.pkl | RF model location |
| `ENCODERS_PATH` | data/models/label_encoders.pkl | LabelEncoders location |
| `SCALER_PATH` | data/models/scaler.pkl | Scaler location |
| `API_PORT` | 8000 | Uvicorn listen port |
| `CORS_ORIGINS` | ["http://localhost:3000"] | Allowed origins |

---

## Vercel (Frontend)

```bash
cd frontend
npm run build
vercel deploy
```

Set `NEXT_PUBLIC_API_URL` to your backend URL in the Vercel dashboard.

---

## Production Checklist

- [ ] Set `DEBUG=false` and `LOG_LEVEL=INFO`
- [ ] Mount `data/models/` as a persistent volume
- [ ] Run `train_model.py` before first API start
- [ ] Configure `CORS_ORIGINS` to match your frontend domain
- [ ] Enable Docker health check monitoring
- [ ] Set `--workers 4` in uvicorn CMD for multi-core hosts
