"""
Production-ready training pipeline for the matchmaking engine.
"""

import joblib
import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

from app.core.constants import (
    RANDOM_STATE,
    RF_MAX_DEPTH,
    RF_N_ESTIMATORS,
    TEST_SIZE,
)
from app.logging_config import get_logger
from app.services.matchmaking.feature_engineering import TARGET_COLUMN
from app.services.matchmaking.preprocessing import MatchmakingPreprocessor

logger = get_logger(__name__)


class ModelTrainer:
    """
    End-to-end ML training pipeline.
    """

    def __init__(self) -> None:
        self.model = RandomForestClassifier(
            n_estimators=RF_N_ESTIMATORS,
            max_depth=RF_MAX_DEPTH,
            class_weight="balanced",
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )
        self.preprocessor = MatchmakingPreprocessor()

    def train(
        self,
        dataset_path: str,
        model_output_path: str = "data/models/matcher_model.pkl",
        encoders_output_path: str = "data/models/label_encoders.pkl",
        scaler_output_path: str = "data/models/scaler.pkl",
    ) -> dict:
        logger.info("training_started", dataset=dataset_path)

        df = pd.read_csv(dataset_path)
        logger.info("dataset_loaded", rows=len(df))

        X = df.drop(columns=[TARGET_COLUMN])
        y = df[TARGET_COLUMN]

        X_processed = self.preprocessor.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_processed,
            y,
            test_size=TEST_SIZE,
            stratify=y,
            random_state=RANDOM_STATE,
        )

        logger.info(
            "train_test_split_complete",
            train_size=len(X_train),
            test_size=len(X_test),
        )

        smote = SMOTE(random_state=RANDOM_STATE)
        X_train_balanced, y_train_balanced = smote.fit_resample(
            X_train,
            y_train,
        )

        logger.info(
            "smote_complete",
            balanced_size=len(X_train_balanced),
        )

        self.model.fit(X_train_balanced, y_train_balanced)

        predictions = self.model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions, output_dict=True)

        logger.info("training_complete", accuracy=round(accuracy, 4))

        Path(model_output_path).parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.model, model_output_path)
        self.preprocessor.save(
            encoders_output_path,
            scaler_output_path,
        )

        logger.info("artefacts_saved")

        return {
            "accuracy": accuracy,
            "report": report,
            "model_path": model_output_path,
        }
