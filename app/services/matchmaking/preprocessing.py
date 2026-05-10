"""
Preprocessing pipeline: encode categoricals + scale numericals.

The preprocessor is stateful (fitted once on training data, then
serialised). It must not be re-fitted at inference time.
"""

import joblib
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from app.services.matchmaking.feature_engineering import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
    add_derived_features,
    get_feature_columns,
)
from app.core.exceptions import PreprocessingError
from app.logging_config import get_logger

logger = get_logger(__name__)

_DERIVED = ["experience_ratio", "skill_win_interaction"]
_SCALED_COLS = NUMERICAL_FEATURES + _DERIVED


class MatchmakingPreprocessor:
    """
    Stateful preprocessing pipeline.

    Usage:
        # Training
        p = MatchmakingPreprocessor()
        X = p.fit_transform(df)
        p.save("data/models/label_encoders.pkl", "data/models/scaler.pkl")

        # Inference
        p = MatchmakingPreprocessor.load(...)
        X = p.transform(record_dict)
    """

    def __init__(self) -> None:
        self.encoders: dict[str, LabelEncoder] = {}
        self.scaler = MinMaxScaler()
        self._fitted = False

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = add_derived_features(df.copy())

        for col in CATEGORICAL_FEATURES:
            enc = LabelEncoder()
            df[col] = enc.fit_transform(df[col].astype(str))
            self.encoders[col] = enc

        df[_SCALED_COLS] = self.scaler.fit_transform(df[_SCALED_COLS])
        self._fitted = True

        logger.info(
            "preprocessor_fitted",
            categorical_cols=CATEGORICAL_FEATURES,
            scaled_cols=_SCALED_COLS,
        )
        return df[get_feature_columns()]

    def transform(self, record: dict) -> pd.DataFrame:
        if not self._fitted:
            raise PreprocessingError("Preprocessor not fitted. Load a saved preprocessor first.")

        df = pd.DataFrame([record])
        df = add_derived_features(df)

        for col in CATEGORICAL_FEATURES:
            if col not in self.encoders:
                raise PreprocessingError(f"No encoder found for column '{col}'.")
            try:
                df[col] = self.encoders[col].transform(df[col].astype(str))
            except ValueError as e:
                raise PreprocessingError(
                    f"Unknown category in column '{col}': {df[col].values[0]}"
                ) from e

        df[_SCALED_COLS] = self.scaler.transform(df[_SCALED_COLS])
        return df[get_feature_columns()]

    def save(self, encoders_path: str, scaler_path: str) -> None:
        Path(encoders_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.encoders, encoders_path)
        joblib.dump(self.scaler, scaler_path)
        logger.info("preprocessor_saved", encoders_path=encoders_path, scaler_path=scaler_path)

    @classmethod
    def load(cls, encoders_path: str, scaler_path: str) -> "MatchmakingPreprocessor":
        instance = cls()
        instance.encoders = joblib.load(encoders_path)
        instance.scaler = joblib.load(scaler_path)
        instance._fitted = True
        logger.info("preprocessor_loaded", encoders_path=encoders_path, scaler_path=scaler_path)
        return instance
