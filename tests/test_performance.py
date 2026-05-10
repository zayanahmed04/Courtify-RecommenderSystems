"""
Performance benchmarks for A* search.
Run with: pytest tests/test_performance.py -v -s
"""

import time
import pytest
from app.models.court import Court, CourtSearchQuery
from app.services.court_search.astar_engine import AStarCourtSearch
from app.core.exceptions import NoCourtsFoundError


def _make_courts(n: int) -> list[Court]:
    sports = ["Padel", "Cricket", "Football", "Badminton", "Basketball"]
    return [
        Court(
            id=i,
            name=f"Court {i}",
            sport=sports[i % len(sports)],
            latitude=24.86 + (i % 50) * 0.01,
            longitude=67.00 + (i % 50) * 0.01,
            price_per_hour=500 + (i % 10) * 200,
            rating=round(3.0 + (i % 20) * 0.1, 1),
            available_slots=["6PM"],
        )
        for i in range(n)
    ]


class TestAStarPerformance:
    @pytest.mark.parametrize("court_count", [100, 500, 1000, 5000])
    def test_search_latency_under_threshold(self, court_count: int):
        courts = _make_courts(court_count)
        engine = AStarCourtSearch(courts)
        query = CourtSearchQuery(
            sport="Padel", budget=5000, location=(24.8607, 67.0011)
        )

        start = time.perf_counter()
        try:
            result = engine.search(query)
        except NoCourtsFoundError:
            pytest.skip("No Padel courts in generated set")
        elapsed = time.perf_counter() - start

        # Should complete well under 500ms even for 5000 courts
        assert elapsed < 0.5, f"A* took {elapsed:.3f}s for {court_count} courts"
        print(f"\n  {court_count} courts: {elapsed * 1000:.2f}ms | results: {result.total_found}")

    def test_deterministic_results(self):
        courts = _make_courts(200)
        engine = AStarCourtSearch(courts)
        query = CourtSearchQuery(sport="Padel", budget=5000, location=(24.8607, 67.0011))

        try:
            r1 = engine.search(query)
            r2 = engine.search(query)
        except NoCourtsFoundError:
            pytest.skip("No Padel courts in generated set")

        assert [r.court for r in r1.recommendations] == [r.court for r in r2.recommendations]
        assert [r.score for r in r1.recommendations] == [r.score for r in r2.recommendations]
