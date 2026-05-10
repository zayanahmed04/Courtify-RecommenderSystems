from app.models.court import Court, CourtSearchQuery
from app.core.exceptions import InvalidPlayerQueryError, UnsupportedSportError
from app.core.constants import SUPPORTED_SPORTS


def validate_query(query: CourtSearchQuery) -> None:
    if query.sport not in SUPPORTED_SPORTS:
        raise UnsupportedSportError(f"Sport '{query.sport}' is not supported.")

    if query.budget <= 0:
        raise InvalidPlayerQueryError("Budget must be a positive number.")

    lat, lon = query.location
    if not (-90 <= lat <= 90):
        raise InvalidPlayerQueryError(f"Invalid latitude: {lat}")
    if not (-180 <= lon <= 180):
        raise InvalidPlayerQueryError(f"Invalid longitude: {lon}")


def filter_candidates(courts: list[Court], query: CourtSearchQuery) -> list[Court]:
    """Apply hard filters before A* scoring."""
    return [
        c for c in courts
        if c.sport == query.sport and c.price_per_hour <= query.budget
    ]
