from fastapi import Depends
from app.services.matchmaking.inference import MatchmakingInference, inference_engine
from app.services.court_search.astar_engine import AStarCourtSearch
from app.models.court import Court
from app.core.constants import SUPPORTED_SPORTS


def get_inference_engine() -> MatchmakingInference:
    return inference_engine


def get_sample_courts() -> list[Court]:
    """
    Returns the seeded in-memory court dataset.
    In production, this would be replaced by a database query dependency.
    """
    return [
        Court(
            id=1, name="Padel Arena DHA", sport="Padel",
            latitude=24.7966, longitude=67.0681,
            price_per_hour=1500, rating=4.7,
            available_slots=["6PM", "7PM", "8PM"]
        ),
        Court(
            id=2, name="Clifton Sports Complex", sport="Padel",
            latitude=24.8121, longitude=67.0299,
            price_per_hour=1200, rating=4.2,
            available_slots=["5PM", "6PM"]
        ),
        Court(
            id=3, name="Green Court Badminton", sport="Badminton",
            latitude=24.8607, longitude=67.0011,
            price_per_hour=600, rating=4.5,
            available_slots=["7AM", "8AM", "5PM", "6PM"]
        ),
        Court(
            id=4, name="Korangi Cricket Ground", sport="Cricket",
            latitude=24.8324, longitude=67.1282,
            price_per_hour=800, rating=3.9,
            available_slots=["6AM", "7AM"]
        ),
        Court(
            id=5, name="North Nazimabad Football Club", sport="Football",
            latitude=24.9239, longitude=67.0621,
            price_per_hour=1000, rating=4.1,
            available_slots=["4PM", "5PM", "6PM"]
        ),
        Court(
            id=6, name="Elite Basketball Academy", sport="Basketball",
            latitude=24.8715, longitude=67.0421,
            price_per_hour=900, rating=4.6,
            available_slots=["3PM", "4PM", "7PM"]
        ),
        Court(
            id=7, name="Gulshan Badminton Hall", sport="Badminton",
            latitude=24.9215, longitude=67.0931,
            price_per_hour=500, rating=4.0,
            available_slots=["6AM", "8PM", "9PM"]
        ),
        Court(
            id=8, name="Defence Padel Club", sport="Padel",
            latitude=24.8221, longitude=67.0711,
            price_per_hour=2000, rating=4.9,
            available_slots=["9AM", "10AM", "6PM", "7PM"]
        ),
    ]


def get_court_search_engine(
    courts: list[Court] = Depends(get_sample_courts),
) -> AStarCourtSearch:
    return AStarCourtSearch(courts)
