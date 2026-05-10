import heapq
import time
from dataclasses import dataclass, field
from typing import Any

from app.models.court import Court, CourtSearchQuery
from app.models.response_models import CourtResult, CourtSearchResponse
from app.services.court_search.heuristic import CourtHeuristic, HeuristicWeights
from app.services.court_search.validators import validate_query, filter_candidates
from app.core.constants import ASTAR_MAX_RESULTS
from app.core.exceptions import NoCourtsFoundError
from app.logging_config import get_logger

logger = get_logger(__name__)


@dataclass(order=True)
class _ScoredCourt:
    """Priority queue entry. Ordered by score, then court id (deterministic)."""

    score: float
    court_id: int = field(compare=True)
    court: Any = field(compare=False)
    distance_km: float = field(compare=False, default=0.0)


class AStarCourtSearch:
    """
    A*-inspired court recommendation engine.

    Heuristic h(n) estimates how well a court satisfies the player's
    query across three normalised dimensions:
      - Proximity (distance)
      - Affordability (price)
      - Quality (inverted rating)

    g(n) = 0 for all nodes because this is a single-source ranking
    problem, not a pathfinding problem. The priority queue orders all
    candidates by h(n) alone, which is mathematically equivalent to a
    best-first greedy search — the standard A* pattern when there is no
    cumulative edge cost.

    Why A* framing?
      - Explicit open/closed sets make it trivial to extend to graph
        traversal (e.g. multi-hop routing through court clusters).
      - Heuristic weights are externalised and tunable per request.
      - The closed set prevents re-evaluation of the same court if the
        graph builder exposes it via multiple paths (future-proofing).
    """

    def __init__(
        self,
        courts: list[Court],
        weights: HeuristicWeights | None = None,
    ) -> None:
        self.courts = courts
        self.heuristic = CourtHeuristic(weights)

    def search(self, query: CourtSearchQuery) -> CourtSearchResponse:
        """
        Run A* search and return ranked court recommendations.

        Args:
            query: Validated CourtSearchQuery

        Returns:
            CourtSearchResponse with ranked results

        Raises:
            NoCourtsFoundError: If no courts match the hard filters.
        """
        t_start = time.perf_counter()
        validate_query(query)

        candidates = filter_candidates(self.courts, query)

        logger.info(
            "astar_search_started",
            sport=query.sport,
            budget=query.budget,
            total_courts=len(self.courts),
            candidate_count=len(candidates),
        )

        if not candidates:
            raise NoCourtsFoundError(
                f"No courts found for sport='{query.sport}' within budget={query.budget}."
            )

        open_set: list[_ScoredCourt] = []
        closed: set[int] = set()

        for court in candidates:
            score = self.heuristic.evaluate(query.location, court, query.budget)
            dist = self.heuristic.distance_km(query.location, court)
            heapq.heappush(
                open_set,
                _ScoredCourt(score=score, court_id=court.id, court=court, distance_km=dist),
            )

        results: list[CourtResult] = []
        max_results = min(query.max_results, ASTAR_MAX_RESULTS)

        while open_set and len(results) < max_results:
            entry = heapq.heappop(open_set)

            if entry.court_id in closed:
                continue

            closed.add(entry.court_id)

            results.append(
                CourtResult(
                    court=entry.court.name,
                    score=round(entry.score, 4),
                    rating=entry.court.rating,
                    price=entry.court.price_per_hour,
                    distance_km=round(entry.distance_km, 2),
                    available_slots=entry.court.available_slots,
                )
            )

        elapsed_ms = round((time.perf_counter() - t_start) * 1000, 2)

        logger.info(
            "astar_search_completed",
            results_returned=len(results),
            elapsed_ms=elapsed_ms,
        )

        return CourtSearchResponse(
            query_sport=query.sport,
            budget=query.budget,
            total_found=len(results),
            recommendations=results,
        )
