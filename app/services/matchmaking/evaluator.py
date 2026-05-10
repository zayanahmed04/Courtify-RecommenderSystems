"""
Standalone model evaluator for offline evaluation and monitoring.
"""

import joblib
import pandas as pd
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix,
    f1_score,
)

from app.services.matchmaking.preprocessing import MatchmakingPreprocessor
from app.core.constants import COMPATIBILITY_LABELS
from app.logging_config import get_logger

logger = get_logger(__name__)


class ModelEvaluator:
    """
    Loads a trained model + preprocessor and evaluates on a held-out CSV.
    Used for drift detection and post-deployment evaluation.
    """

    def __init__(
        self,
        model_path: str,
        encoders_path: str,
        scaler_path: str,
    ) -> None:
        self.model = joblib.load(model_path)
        self.preprocessor = MatchmakingPreprocessor.load(encoders_path, scaler_path)
        logger.info("evaluator_loaded")

    def evaluate(self, dataset_path: str) -> dict:
        df = pd.read_csv(dataset_path)
        y_true = df["match_compatibility"]
        X = self.preprocessor.fit_transform(df.drop(columns=["match_compatibility"]))
        # For evaluation, use transform not fit_transform
        df_raw = pd.read_csv(dataset_path)
        y_true = df_raw["match_compatibility"]
        X = self.preprocessor.transform(df_raw.drop(columns=["match_compatibility"]).iloc[0].to_dict())

        # Evaluate row by row using transform
        preds = []
        for _, row in df_raw.drop(columns=["match_compatibility"]).iterrows():
            X_row = self.preprocessor.transform(row.to_dict())
            preds.append(self.model.predict(X_row)[0])

        accuracy = accuracy_score(y_true, preds)
        f1 = f1_score(y_true, preds, average="weighted")
        cm = confusion_matrix(y_true, preds)

        report = {
            "accuracy": round(accuracy, 4),
            "f1_weighted": round(f1, 4),
            "confusion_matrix": cm.tolist(),
            "classification_report": classification_report(
                y_true, preds, output_dict=True
            ),
        }

        logger.info("evaluation_complete", accuracy=accuracy, f1=f1)
        return report
