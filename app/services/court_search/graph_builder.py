from app.models.court import Court
from app.services.shared.distance import haversine_distance
from app.logging_config import get_logger

logger = get_logger(__name__)


class CourtGraph:
    """
    Adjacency graph of courts, pre-filtered by sport.

    Edges represent proximity relationships between courts,
    allowing future extensions (e.g., multi-hop routing or
    cluster-based search). Currently used for candidate set
    construction in A* with neighbour expansion.
    """

    def __init__(self, courts: list[Court], proximity_km: float = 10.0) -> None:
        self.courts = courts
        self.proximity_km = proximity_km
        self._adjacency: dict[int, list[int]] = {}
        self._build()

    def _build(self) -> None:
        for i, a in enumerate(self.courts):
            neighbours = []
            for j, b in enumerate(self.courts):
                if i == j:
                    continue
                dist = haversine_distance(
                    a.latitude, a.longitude, b.latitude, b.longitude
                )
                if dist <= self.proximity_km:
                    neighbours.append(j)
            self._adjacency[i] = neighbours

        logger.debug(
            "court_graph_built",
            total_courts=len(self.courts),
            proximity_km=self.proximity_km,
        )

    def neighbours(self, court_index: int) -> list[Court]:
        return [self.courts[j] for j in self._adjacency.get(court_index, [])]

    def index_of(self, court: Court) -> int | None:
        for i, c in enumerate(self.courts):
            if c.id == court.id:
                return i
        return None
