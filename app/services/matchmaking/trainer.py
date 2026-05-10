"""
Model trainer for the matchmaking Random Forest classifier.

Uses SMOTE to handle class imbalance and stratified train/test splits
for reproducible evaluation.
"""

import joblib
import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

from app.services.matchmaking.preprocessing import MatchmakingPreprocessor
from app.services.matchmaking.feature_engineering import TARGET_COLUMN
from app.core.constants import (
    RANDOM_STATE,
    TEST_SIZE,
    RF_N_ESTIMATORS,
    RF_MAX_DEPTH,
)
from app.logging_config import get_logger

logger = get_logger(__name__)


class ModelTrainer:
    """
    End-to-end training pipeline:
      1. Load CSV
      2. Engineer features
      3. Preprocess (encode + scale)
      4. Balance classes with SMOTE
      5. Train Random Forest
      6. Evaluate
      7. Serialise model + preprocessor artefacts
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
        logger.info("dataset_loaded", rows=len(df), columns=list(df.columns))

        y = df[TARGET_COLUMN]
        df_features = df.drop(columns=[TARGET_COLUMN])

        X = self.preprocessor.fit_transform(df_features.assign(**{TARGET_COLUMN: y}).drop(columns=[TARGET_COLUMN]))
        # Re-process properly: fit_transform on full df minus target
        full_df = df.copy()
        X = self.preprocessor.fit_transform(full_df)
        y = full_df[TARGET_COLUMN] if TARGET_COLUMN in full_df.columns else y

        # After fit_transform the target is stripped — reload
        df_raw = pd.read_csv(dataset_path)
        y = df_raw[TARGET_COLUMN]
        X = self.preprocessor.fit_transform(df_raw.drop(columns=[TARGET_COLUMN]))

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
        )

        logger.info(
            "train_test_split_done",
            train_size=len(X_train),
            test_size=len(X_test),
        )

        smote = SMOTE(random_state=RANDOM_STATE)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

        logger.info(
            "smote_applied",
            original_train_size=len(X_train),
            balanced_train_size=len(X_train_balanced),
        )

        self.model.fit(X_train_balanced, y_train_balanced)

        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions, output_dict=True)

        logger.info("training_complete", accuracy=round(accuracy, 4))
        print("\n" + "=" * 50)
        print(f"  Accuracy: {accuracy:.4f}")
        print("=" * 50)
        print(classification_report(y_test, predictions))

        Path(model_output_path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, model_output_path)
        self.preprocessor.save(encoders_output_path, scaler_output_path)

        logger.info(
            "artefacts_saved",
            model=model_output_path,
            encoders=encoders_output_path,
            scaler=scaler_output_path,
        )

        return {
            "accuracy": accuracy,
            "report": report,
            "model_path": model_output_path,
        }
