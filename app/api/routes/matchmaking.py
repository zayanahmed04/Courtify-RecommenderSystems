from fastapi import APIRouter, Depends, HTTPException, status
from app.models.player import PlayerMatchQuery
from app.models.response_models import MatchPrediction
from app.services.matchmaking.inference import MatchmakingInference
from app.api.dependencies import get_inference_engine
from app.core.exceptions import ModelNotTrainedError, PreprocessingError
from app.logging_config import get_logger

router = APIRouter(tags=["Matchmaking"])
logger = get_logger(__name__)


@router.post(
    "/predict",
    response_model=MatchPrediction,
    summary="Predict player match compatibility",
    description=(
        "Given a player profile, uses a trained Random Forest classifier to "
        "predict match compatibility class (Low / Mid / High) and confidence."
    ),
)
def predict_match(
    payload: PlayerMatchQuery,
    engine: MatchmakingInference = Depends(get_inference_engine),
) -> MatchPrediction:
    try:
        return engine.predict(payload.model_dump())
    except ModelNotTrainedError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except PreprocessingError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("unexpected_error_in_matchmaking", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during matchmaking prediction.",
        )
