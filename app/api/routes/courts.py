from fastapi import APIRouter, Depends, HTTPException, status
from app.models.court import CourtSearchQuery
from app.models.response_models import CourtSearchResponse
from app.services.court_search.astar_engine import AStarCourtSearch
from app.api.dependencies import get_court_search_engine
from app.core.exceptions import (
    NoCourtsFoundError,
    InvalidPlayerQueryError,
    UnsupportedSportError,
)
from app.logging_config import get_logger

router = APIRouter(tags=["Courts"])
logger = get_logger(__name__)


@router.post(
    "/search",
    response_model=CourtSearchResponse,
    summary="Search for courts using A* informed search",
    description=(
        "Given a sport, budget, and player location, returns ranked court "
        "recommendations using a multi-factor A* heuristic (distance, price, rating)."
    ),
)
def search_courts(
    query: CourtSearchQuery,
    engine: AStarCourtSearch = Depends(get_court_search_engine),
) -> CourtSearchResponse:
    try:
        return engine.search(query)
    except (UnsupportedSportError, InvalidPlayerQueryError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NoCourtsFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        logger.exception("unexpected_error_in_court_search", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during court search.",
        )
