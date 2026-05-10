"""
Feature engineering for the matchmaking pipeline.

This module is intentionally kept separate from preprocessing so that
feature definitions can evolve independently of encoding/scaling logic.
"""

import pandas as pd
import numpy as np


CATEGORICAL_FEATURES = [
    "preferred_sport",
    "play_style",
    "age_group",
    "location_zone",
]

NUMERICAL_FEATURES = [
    "skill_level",
    "win_rate",
    "avg_session_duration",
    "games_played",
    "availability_hours",
]

TARGET_COLUMN = "match_compatibility"

ALL_FEATURES = CATEGORICAL_FEATURES + NUMERICAL_FEATURES


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add engineered features before encoding.

    - experience_ratio: games_played normalised by a 500-game ceiling.
    - skill_win_interaction: product of skill_level and win_rate.
    """
    df = df.copy()
    df["experience_ratio"] = (df["games_played"] / 500).clip(0, 1)
    df["skill_win_interaction"] = (df["skill_level"] / 10) * df["win_rate"]
    return df


def get_feature_columns() -> list[str]:
    return CATEGORICAL_FEATURES + NUMERICAL_FEATURES + [
        "experience_ratio",
        "skill_win_interaction",
    ]
