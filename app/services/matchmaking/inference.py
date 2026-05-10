"""
Inference engine — loaded once at startup, reused across requests.

Lazy-loads model artefacts only on first call so the API can start
even before training has been run (it will return a clear error).
"""

import joblib
import time
from functools import cached_property

from app.services.matchmaking.preprocessing import MatchmakingPreprocessor
from app.models.response_models import MatchPrediction
from app.core.constants import COMPATIBILITY_LABELS
from app.core.exceptions import ModelNotTrainedError
from app.config import settings
from app.logging_config import get_logger

logger = get_logger(__name__)

_RECOMMENDATIONS = {
    0: "Consider players in a similar skill range to build experience before higher-stakes matches.",
    1: "A balanced match — expect a competitive but fair game.",
    2: "Excellent compatibility — this should be a high-quality, well-matched game.",
}


class MatchmakingInference:
    """
    Inference wrapper around the trained Random Forest.

    Thread-safe for concurrent FastAPI request handling because
    scikit-learn `predict` releases the GIL and model state is read-only.
    """

    def __init__(self) -> None:
        self._model = None
        self._preprocessor: MatchmakingPreprocessor | None = None
        self._ready = False

    def _load(self) -> None:
        if self._ready:
            return

        if not settings.model_paths_exist():
            raise ModelNotTrainedError(
                "Model artefacts not found. Run `python scripts/train_model.py` first."
            )

        self._model = joblib.load(settings.MODEL_PATH)
        self._preprocessor = MatchmakingPreprocessor.load(
            settings.ENCODERS_PATH, settings.SCALER_PATH
        )
        self._ready = True
        logger.info("inference_engine_loaded", model_path=settings.MODEL_PATH)

    def predict(self, player: dict) -> MatchPrediction:
        self._load()

        t_start = time.perf_counter()
        X = self._preprocessor.transform(player)

        pred_class = int(self._model.predict(X)[0])
        confidence = float(self._model.predict_proba(X).max())

        elapsed_ms = round((time.perf_counter() - t_start) * 1000, 2)

        logger.info(
            "inference_done",
            compatibility_class=pred_class,
            confidence=round(confidence, 4),
            elapsed_ms=elapsed_ms,
        )

        return MatchPrediction(
            compatibility_class=pred_class,
            compatibility_label=COMPATIBILITY_LABELS.get(pred_class, "Unknown"),
            confidence=round(confidence, 4),
            recommendation=_RECOMMENDATIONS.get(pred_class, ""),
        )

    @property
    def ready(self) -> bool:
        return self._ready


# Module-level singleton — imported by the route and dependency injection
inference_engine = MatchmakingInference()
