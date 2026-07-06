"""Application configuration.

Settings are read from environment variables (and an optional `.env` file),
with sensible defaults so the app runs out of the box.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Identity
    app_name: str = "IntelliSight"
    version: str = "0.5.0"
    environment: str = "development"

    # Server
    host: str = "127.0.0.1"
    port: int = 8000

    # Comma-separated list of allowed frontend origins.
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Object detection (YOLO)
    yolo_model: str = "yolov8n.pt"      # nano — small & fast; auto-downloaded
    detection_conf: float = 0.35        # minimum confidence to report a box
    detection_device: str = "cpu"       # "cpu" or "mps" (Apple GPU)
    detection_imgsz: int = 640          # inference image size

    @property
    def cors_origins_list(self) -> list[str]:
        """The CORS origins parsed into a clean list."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (read once, reused everywhere)."""
    return Settings()
