"""Health & status endpoints — used to confirm the backend is alive."""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import get_settings

router = APIRouter(tags=["system"])
settings = get_settings()


@router.get("/health", summary="Liveness check")
def health() -> dict:
    """Return a simple 'I am alive' payload."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "time": datetime.now(timezone.utc).isoformat(),
    }
