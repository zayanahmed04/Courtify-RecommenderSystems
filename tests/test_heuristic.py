import pytest
from app.services.court_search.heuristic import CourtHeuristic, HeuristicWeights
from app.services.shared.metrics import normalize, clamp, weighted_sum
from app.services.shared.distance import haversine_distance
from app.models.court import Court


class TestHaversineDistance:
    def test_same_location_is_zero(self):
        assert haversine_distance(24.86, 67.00, 24.86, 67.00) == 0.0

    def test_karachi_to_lahore_approx(self):
        # Karachi (~24.86, ~67.01) to Lahore (~31.55, ~74.35) ≈ 1050 km
        dist = haversine_distance(24.86, 67.01, 31.55, 74.35)
        assert 900 < dist < 1200

    def test_result_is_positive(self):
        dist = haversine_distance(24.86, 67.00, 24.90, 67.10)
        assert dist > 0


class TestMetrics:
    def test_normalize_mid(self):
        assert normalize(5, 0, 10) == pytest.approx(0.5)

    def test_normalize_at_min(self):
        assert normalize(0, 0, 10) == pytest.approx(0.0)

    def test_normalize_at_max(self):
        assert normalize(10, 0, 10) == pytest.approx(1.0)

    def test_normalize_safe_zero_range(self):
        assert normalize(5, 5, 5) == 0.0

    def test_clamp_within(self):
        assert clamp(0.5) == pytest.approx(0.5)

    def test_clamp_below(self):
        assert clamp(-1.0) == pytest.approx(0.0)

    def test_clamp_above(self):
        assert clamp(2.0) == pytest.approx(1.0)

    def test_weighted_sum_equal_weights(self):
        result = weighted_sum([(1.0, 1.0), (0.0, 1.0)])
        assert result == pytest.approx(0.5)
