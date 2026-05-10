import pytest
from app.models.court import Court, CourtSearchQuery
from app.services.court_search.astar_engine import AStarCourtSearch
from app.services.court_search.heuristic import CourtHeuristic, HeuristicWeights
from app.core.exceptions import NoCourtsFoundError, UnsupportedSportError


SAMPLE_COURTS = [
    Court(
        id=1, name="Arena A", sport="Padel",
        latitude=24.8607, longitude=67.0011,
        price_per_hour=1200, rating=4.5,
        available_slots=["6PM"]
    ),
    Court(
        id=2, name="Arena B", sport="Padel",
        latitude=24.8700, longitude=67.0100,
        price_per_hour=800, rating=4.0,
        available_slots=["5PM"]
    ),
    Court(
        id=3, name="Cricket Ground X", sport="Cricket",
        latitude=24.8500, longitude=67.0200,
        price_per_hour=600, rating=3.8,
        available_slots=["7AM"]
    ),
]


class TestAStarCourtSearch:
    def test_returns_results_for_valid_query(self):
        engine = AStarCourtSearch(SAMPLE_COURTS)
        query = CourtSearchQuery(sport="Padel", budget=2000, location=(24.8607, 67.0011))
        response = engine.search(query)
        assert len(response.recommendations) > 0

    def test_filters_by_sport(self):
        engine = AStarCourtSearch(SAMPLE_COURTS)
        query = CourtSearchQuery(sport="Cricket", budget=2000, location=(24.8607, 67.0011))
        response = engine.search(query)
        # Only Cricket courts should appear — Arena A/B are Padel
        assert response.total_found == 1

    def test_filters_by_budget(self):
        engine = AStarCourtSearch(SAMPLE_COURTS)
        # Budget 700 should exclude Arena A (1200) but include Arena B (800)... wait 800 > 700
        # Only should return 0 Padel results
        query = CourtSearchQuery(sport="Padel", budget=700, location=(24.8607, 67.0011))
        with pytest.raises(NoCourtsFoundError):
            engine.search(query)

    def test_raises_on_no_candidates(self):
        engine = AStarCourtSearch([])
        query = CourtSearchQuery(sport="Padel", budget=2000, location=(24.8607, 67.0011))
        with pytest.raises(NoCourtsFoundError):
            engine.search(query)

    def test_respects_max_results(self):
        engine = AStarCourtSearch(SAMPLE_COURTS)
        query = CourtSearchQuery(
            sport="Padel", budget=2000, location=(24.8607, 67.0011), max_results=1
        )
        response = engine.search(query)
        assert len(response.recommendations) <= 1

    def test_results_ordered_by_score_ascending(self):
        engine = AStarCourtSearch(SAMPLE_COURTS)
        query = CourtSearchQuery(sport="Padel", budget=2000, location=(24.8607, 67.0011))
        response = engine.search(query)
        scores = [r.score for r in response.recommendations]
        assert scores == sorted(scores)

    def test_distance_km_populated(self):
        engine = AStarCourtSearch(SAMPLE_COURTS)
        query = CourtSearchQuery(sport="Padel", budget=2000, location=(24.8607, 67.0011))
        response = engine.search(query)
        for result in response.recommendations:
            assert result.distance_km is not None
            assert result.distance_km >= 0


class TestHeuristic:
    def test_weights_must_sum_to_one(self):
        with pytest.raises(ValueError):
            HeuristicWeights(distance=0.6, price=0.3, rating=0.2)

    def test_score_between_zero_and_one(self):
        h = CourtHeuristic()
        court = SAMPLE_COURTS[0]
        score = h.evaluate((24.8607, 67.0011), court, 2000)
        assert 0.0 <= score <= 1.0

    def test_closer_court_has_lower_score(self):
        h = CourtHeuristic(HeuristicWeights(distance=1.0, price=0.0, rating=0.0))
        close = Court(
            id=10, name="Close", sport="Padel",
            latitude=24.8610, longitude=67.0015,
            price_per_hour=1000, rating=4.0, available_slots=[]
        )
        far = Court(
            id=11, name="Far", sport="Padel",
            latitude=25.5000, longitude=68.0000,
            price_per_hour=1000, rating=4.0, available_slots=[]
        )
        player_loc = (24.8607, 67.0011)
        assert h.evaluate(player_loc, close, 2000) < h.evaluate(player_loc, far, 2000)
