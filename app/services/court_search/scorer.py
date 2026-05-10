from app.models.court import Court
from app.services.court_search.heuristic import CourtHeuristic


class CourtScorer:
    """
    Utility for scoring individual courts outside of a full A* search.
    Useful for debugging, auditing, and benchmarking the heuristic.
    """

    def __init__(self) -> None:
        self.heuristic = CourtHeuristic()

    def score_all(
        self,
        courts: list[Court],
        player_location: tuple[float, float],
        budget: float,
    ) -> list[dict]:
        results = []
        for court in courts:
            score = self.heuristic.evaluate(player_location, court, budget)
            dist = self.heuristic.distance_km(player_location, court)
            results.append(
                {
                    "id": court.id,
                    "name": court.name,
                    "score": score,
                    "distance_km": round(dist, 2),
                    "price": court.price_per_hour,
                    "rating": court.rating,
                }
            )
        return sorted(results, key=lambda x: x["score"])
