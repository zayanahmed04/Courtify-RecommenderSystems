from dataclasses import dataclass
from app.services.shared.distance import haversine_distance
from app.services.shared.metrics import clamp
from app.core.constants import (
    HEURISTIC_WEIGHT_DISTANCE,
    HEURISTIC_WEIGHT_PRICE,
    HEURISTIC_WEIGHT_RATING,
    ASTAR_MAX_DISTANCE_KM,
)


@dataclass
class HeuristicWeights:
    distance: float = HEURISTIC_WEIGHT_DISTANCE
    price: float = HEURISTIC_WEIGHT_PRICE
    rating: float = HEURISTIC_WEIGHT_RATING

    def __post_init__(self) -> None:
        total = self.distance + self.price + self.rating
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Heuristic weights must sum to 1.0, got {total:.4f}"
            )


class CourtHeuristic:
    """
    Multi-factor heuristic for A* court scoring.

    Lower score = better court (treated as cost in the priority queue).

    Components:
      - Normalized distance  (closer is better → lower score)
      - Normalized price     (cheaper is better → lower score)
      - Inverted rating      (higher rating is better → lower score)
    """

    def __init__(self, weights: HeuristicWeights | None = None) -> None:
        self.weights = weights or HeuristicWeights()

    def evaluate(
        self,
        player_location: tuple[float, float],
        court,
        budget: float,
    ) -> float:
        """
        Compute heuristic score for a single court.

        Args:
            player_location: (lat, lon)
            court: Court model instance
            budget: Player's max price per hour

        Returns:
            Score in [0, 1]. Lower is a better match.
        """
        distance_km = haversine_distance(
            player_location[0],
            player_location[1],
            court.latitude,
            court.longitude,
        )

        norm_distance = clamp(distance_km / ASTAR_MAX_DISTANCE_KM)
        norm_price = clamp(court.price_per_hour / budget) if budget > 0 else 1.0
        norm_rating = clamp(1.0 - court.rating / 5.0)

        score = (
            self.weights.distance * norm_distance
            + self.weights.price * norm_price
            + self.weights.rating * norm_rating
        )

        return round(score, 6)

    def distance_km(
        self,
        player_location: tuple[float, float],
        court,
    ) -> float:
        return haversine_distance(
            player_location[0],
            player_location[1],
            court.latitude,
            court.longitude,
        )
