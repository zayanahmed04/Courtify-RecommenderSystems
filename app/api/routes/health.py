from fastapi import APIRouter
from app.models.response_models import HealthResponse
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service=settings.APP_NAME,
        version="1.0.0",
        model_ready=settings.model_paths_exist(),
    )
