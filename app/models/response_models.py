from pydantic import BaseModel
from typing import Any


class HealthResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    status: str
    service: str
    version: str
    model_ready: bool


class CourtResult(BaseModel):
    court: str
    score: float
    rating: float
    price: float
    distance_km: float | None = None
    available_slots: list[str] = []


class CourtSearchResponse(BaseModel):
    query_sport: str
    budget: float
    total_found: int
    recommendations: list[CourtResult]


class MatchPrediction(BaseModel):
    compatibility_class: int
    compatibility_label: str
    confidence: float
    recommendation: str


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
    code: int
