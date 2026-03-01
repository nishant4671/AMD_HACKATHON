from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./aewis.db"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: List[str] = [
        "http://localhost:8501",
        "https://*.streamlit.app",
        "http://localhost:3000",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
