from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.health import router as health_router
from app.api.routes.courts import router as courts_router
from app.api.routes.matchmaking import router as matchmaking_router
from app.config import settings
from app.logging_config import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description=(
            "AI-powered sports court discovery and player matchmaking engine. "
            "Uses A* informed search for court recommendations and a Random Forest "
            "classifier for match compatibility prediction."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception("unhandled_exception", path=request.url.path, error=str(exc))
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(exc)},
        )

    app.include_router(health_router)
    app.include_router(courts_router, prefix="/courts")
    app.include_router(matchmaking_router, prefix="/matchmaking")

    @app.get("/", tags=["Root"])
    def root():
        return {
            "service": settings.APP_NAME,
            "status": "running",
            "version": "1.0.0",
            "docs": "/docs",
        }

    logger.info("app_created", name=settings.APP_NAME)
    return app


app = create_app()
