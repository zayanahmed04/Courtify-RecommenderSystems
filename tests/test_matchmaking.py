import pytest
import pandas as pd
from app.services.matchmaking.dataset_generator import generate_dataset
from app.services.matchmaking.preprocessing import MatchmakingPreprocessor
from app.services.matchmaking.feature_engineering import (
    get_feature_columns,
    add_derived_features,
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
)


class TestDatasetGenerator:
    def test_generates_correct_size(self):
        df = generate_dataset(size=100, output_path="/tmp/test_dataset.csv", seed=99)
        assert len(df) == 100

    def test_has_required_columns(self):
        df = generate_dataset(size=50, output_path="/tmp/test_dataset.csv", seed=1)
        required = [
            "skill_level", "preferred_sport", "play_style",
            "availability_hours", "avg_session_duration", "win_rate",
            "age_group", "location_zone", "games_played", "match_compatibility"
        ]
        for col in required:
            assert col in df.columns

    def test_compatibility_labels_are_valid(self):
        df = generate_dataset(size=200, output_path="/tmp/test_dataset.csv", seed=2)
        assert set(df["match_compatibility"].unique()).issubset({0, 1, 2})

    def test_all_three_classes_present(self):
        df = generate_dataset(size=500, output_path="/tmp/test_dataset.csv", seed=42)
        assert len(df["match_compatibility"].unique()) == 3


class TestFeatureEngineering:
    def test_derived_features_added(self):
        df = generate_dataset(size=10, output_path="/tmp/test_fe.csv", seed=5)
        df2 = add_derived_features(df)
        assert "experience_ratio" in df2.columns
        assert "skill_win_interaction" in df2.columns

    def test_experience_ratio_clamped(self):
        df = generate_dataset(size=100, output_path="/tmp/test_fe2.csv", seed=6)
        df2 = add_derived_features(df)
        assert (df2["experience_ratio"] >= 0).all()
        assert (df2["experience_ratio"] <= 1).all()


class TestPreprocessor:
    def _get_sample_df(self):
        return generate_dataset(size=100, output_path="/tmp/prep_test.csv", seed=7)

    def test_fit_transform_returns_correct_columns(self):
        df = self._get_sample_df()
        p = MatchmakingPreprocessor()
        X = p.fit_transform(df.drop(columns=["match_compatibility"]))
        expected_cols = set(get_feature_columns())
        assert expected_cols == set(X.columns)

    def test_transform_single_record(self):
        df = self._get_sample_df()
        p = MatchmakingPreprocessor()
        p.fit_transform(df.drop(columns=["match_compatibility"]))
        record = df.drop(columns=["match_compatibility"]).iloc[0].to_dict()
        X = p.transform(record)
        assert X.shape[0] == 1

    def test_transform_raises_on_unfitted(self):
        from app.core.exceptions import PreprocessingError
        p = MatchmakingPreprocessor()
        with pytest.raises(PreprocessingError):
            p.transform({"skill_level": 5})
