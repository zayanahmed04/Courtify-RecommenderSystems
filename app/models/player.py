from pydantic import BaseModel, Field, field_validator
from app.core.constants import SUPPORTED_SPORTS, PLAY_STYLES, AGE_GROUPS, LOCATION_ZONES


class Player(BaseModel):
    id: int
    skill_level: int = Field(..., ge=1, le=10)
    preferred_sport: str
    play_style: str
    availability_hours: int = Field(..., ge=1, le=24)
    avg_session_duration: int = Field(..., ge=15, le=300, description="Minutes")
    win_rate: float = Field(..., ge=0.0, le=1.0)
    age_group: str
    location_zone: str
    games_played: int = Field(..., ge=0)

    @field_validator("preferred_sport")
    @classmethod
    def sport_must_be_supported(cls, v: str) -> str:
        if v not in SUPPORTED_SPORTS:
            raise ValueError(f"Unsupported sport: {v}")
        return v

    @field_validator("play_style")
    @classmethod
    def play_style_must_be_valid(cls, v: str) -> str:
        if v not in PLAY_STYLES:
            raise ValueError(f"Invalid play style: {v}")
        return v

    @field_validator("age_group")
    @classmethod
    def age_group_must_be_valid(cls, v: str) -> str:
        if v not in AGE_GROUPS:
            raise ValueError(f"Invalid age group: {v}")
        return v

    @field_validator("location_zone")
    @classmethod
    def location_zone_must_be_valid(cls, v: str) -> str:
        if v not in LOCATION_ZONES:
            raise ValueError(f"Invalid location zone: {v}")
        return v


class PlayerMatchQuery(BaseModel):
    skill_level: int = Field(..., ge=1, le=10)
    preferred_sport: str
    play_style: str
    availability_hours: int = Field(..., ge=1, le=24)
    avg_session_duration: int = Field(..., ge=15, le=300)
    win_rate: float = Field(..., ge=0.0, le=1.0)
    age_group: str
    location_zone: str
    games_played: int = Field(..., ge=0)

    @field_validator("preferred_sport")
    @classmethod
    def sport_must_be_supported(cls, v: str) -> str:
        if v not in SUPPORTED_SPORTS:
            raise ValueError(f"Unsupported sport: {v}")
        return v

    @field_validator("play_style")
    @classmethod
    def play_style_must_be_valid(cls, v: str) -> str:
        if v not in PLAY_STYLES:
            raise ValueError(f"Invalid play style: {v}")
        return v

    @field_validator("age_group")
    @classmethod
    def age_group_must_be_valid(cls, v: str) -> str:
        if v not in AGE_GROUPS:
            raise ValueError(f"Invalid age group: {v}")
        return v

    @field_validator("location_zone")
    @classmethod
    def location_zone_must_be_valid(cls, v: str) -> str:
        if v not in LOCATION_ZONES:
            raise ValueError(f"Invalid location zone: {v}")
        return v
