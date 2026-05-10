from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    APP_NAME: str = "CourtFind AI"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    MODEL_PATH: str = "data/models/matcher_model.pkl"
    ENCODERS_PATH: str = "data/models/label_encoders.pkl"
    SCALER_PATH: str = "data/models/scaler.pkl"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def model_paths_exist(self) -> bool:
        return all(
            Path(p).exists()
            for p in [self.MODEL_PATH, self.ENCODERS_PATH, self.SCALER_PATH]
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
