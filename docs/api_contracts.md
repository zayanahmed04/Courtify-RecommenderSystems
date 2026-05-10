# CourtFind AI — API Contracts

Base URL: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

---

## GET /health

**Response 200**
```json
{
  "status": "healthy",
  "service": "CourtFind AI",
  "version": "1.0.0",
  "model_ready": true
}
```

---

## POST /courts/search

**Request Body**
```json
{
  "sport": "Padel",
  "budget": 1500,
  "location": [24.8607, 67.0011],
  "max_results": 3
}
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `sport` | string | ✅ | One of: Cricket, Football, Padel, Badminton, Basketball |
| `budget` | float | ✅ | Max price per hour (PKR) |
| `location` | [lat, lon] | ✅ | Player's GPS coordinates |
| `max_results` | int | ❌ | Default 3, max 5 |

**Response 200**
```json
{
  "query_sport": "Padel",
  "budget": 1500.0,
  "total_found": 2,
  "recommendations": [
    {
      "court": "Clifton Sports Complex",
      "score": 0.2341,
      "rating": 4.2,
      "price": 1200.0,
      "distance_km": 3.41,
      "available_slots": ["5PM", "6PM"]
    }
  ]
}
```

**Error Responses**
| Status | When |
|--------|------|
| 400 | Invalid sport or location |
| 404 | No courts match sport + budget |
| 422 | Missing or malformed request fields |

---

## POST /matchmaking/predict

**Request Body**
```json
{
  "skill_level": 7,
  "preferred_sport": "Padel",
  "play_style": "Balanced",
  "availability_hours": 10,
  "avg_session_duration": 90,
  "win_rate": 0.75,
  "age_group": "Young Adult",
  "location_zone": "South",
  "games_played": 120
}
```

| Field | Type | Constraints |
|-------|------|-------------|
| `skill_level` | int | 1–10 |
| `preferred_sport` | string | Supported sports only |
| `play_style` | string | Aggressive / Defensive / Balanced |
| `availability_hours` | int | 1–24 |
| `avg_session_duration` | int | 15–300 minutes |
| `win_rate` | float | 0.0–1.0 |
| `age_group` | string | Teen / Young Adult / Adult / Senior |
| `location_zone` | string | North / South / Central / East / West |
| `games_played` | int | ≥ 0 |

**Response 200**
```json
{
  "compatibility_class": 2,
  "compatibility_label": "High",
  "confidence": 0.8712,
  "recommendation": "Excellent compatibility — this should be a high-quality, well-matched game."
}
```

**Error Responses**
| Status | When |
|--------|------|
| 422 | Invalid field values |
| 503 | Model artefacts not found (run training first) |
