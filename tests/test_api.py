import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_expected_fields(self):
        data = client.get("/health").json()
        assert "status" in data
        assert "service" in data
        assert "model_ready" in data
        assert data["status"] == "healthy"


class TestRootEndpoint:
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_has_service_field(self):
        data = client.get("/").json()
        assert "service" in data


class TestCourtSearchEndpoint:
    def _valid_payload(self):
        return {
            "sport": "Padel",
            "budget": 2000,
            "location": [24.8607, 67.0011],
            "max_results": 3,
        }

    def test_search_returns_200(self):
        response = client.post("/courts/search", json=self._valid_payload())
        assert response.status_code == 200

    def test_search_returns_recommendations(self):
        data = client.post("/courts/search", json=self._valid_payload()).json()
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    def test_search_invalid_sport_returns_422(self):
        payload = self._valid_payload()
        payload["sport"] = "InvalidSport"
        response = client.post("/courts/search", json=payload)
        assert response.status_code == 422

    def test_search_budget_exceeded_returns_404(self):
        payload = self._valid_payload()
        payload["budget"] = 1  # Too low for any court
        response = client.post("/courts/search", json=payload)
        assert response.status_code == 404

    def test_search_results_have_required_fields(self):
        data = client.post("/courts/search", json=self._valid_payload()).json()
        for rec in data["recommendations"]:
            assert "court" in rec
            assert "score" in rec
            assert "rating" in rec
            assert "price" in rec


class TestMatchmakingEndpoint:
    def _valid_payload(self):
        return {
            "skill_level": 7,
            "preferred_sport": "Padel",
            "play_style": "Balanced",
            "availability_hours": 10,
            "avg_session_duration": 90,
            "win_rate": 0.75,
            "age_group": "Young Adult",
            "location_zone": "South",
            "games_played": 120,
        }

    def test_predict_returns_valid_response_or_503(self):
        # Returns 200 if model trained, 503 if artefacts missing
        response = client.post("/matchmaking/predict", json=self._valid_payload())
        assert response.status_code in (200, 503)
        if response.status_code == 200:
            data = response.json()
            assert "compatibility_class" in data
            assert "compatibility_label" in data
            assert "confidence" in data
            assert data["compatibility_class"] in (0, 1, 2)

    def test_predict_invalid_sport_returns_422(self):
        payload = self._valid_payload()
        payload["preferred_sport"] = "Squash"
        response = client.post("/matchmaking/predict", json=payload)
        assert response.status_code == 422

    def test_predict_invalid_skill_level_returns_422(self):
        payload = self._valid_payload()
        payload["skill_level"] = 15  # max is 10
        response = client.post("/matchmaking/predict", json=payload)
        assert response.status_code == 422
