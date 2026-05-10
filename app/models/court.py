from pydantic import BaseModel, Field, field_validator
from app.core.constants import SUPPORTED_SPORTS


class Court(BaseModel):
    id: int
    name: str
    sport: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    price_per_hour: float = Field(..., gt=0)
    rating: float = Field(..., ge=0, le=5)
    available_slots: list[str] = Field(default_factory=list)

    @field_validator("sport")
    @classmethod
    def sport_must_be_supported(cls, v: str) -> str:
        if v not in SUPPORTED_SPORTS:
            raise ValueError(f"Sport '{v}' not supported. Choose from: {SUPPORTED_SPORTS}")
        return v

    @field_validator("rating")
    @classmethod
    def rating_precision(cls, v: float) -> float:
        return round(v, 1)


class CourtSearchQuery(BaseModel):
    sport: str
    budget: float = Field(..., gt=0, description="Max price per hour in PKR")
    location: tuple[float, float] = Field(
        ..., description="(latitude, longitude) of player"
    )
    max_results: int = Field(default=3, ge=1, le=10)

    @field_validator("sport")
    @classmethod
    def sport_must_be_supported(cls, v: str) -> str:
        if v not in SUPPORTED_SPORTS:
            raise ValueError(f"Unsupported sport: {v}")
        return v
