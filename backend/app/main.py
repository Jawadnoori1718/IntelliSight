"""IntelliSight backend — FastAPI application entry point.

Run it with:
    uvicorn app.main:app --reload
or use the convenience script:
    ./run.sh
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import health

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(name)s  %(message)s",
)
logger = logging.getLogger("intellisight")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    logger.info(
        "👁️  %s v%s starting (environment=%s)",
        settings.app_name,
        settings.version,
        settings.environment,
    )
    yield
    logger.info("👋  %s shutting down", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="An AI-powered real-time visual intelligence assistant.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)


@app.get("/", tags=["root"], summary="Welcome")
def root() -> dict:
    """Root endpoint — a friendly hello and pointers to the API."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "message": "👁️  IntelliSight backend is alive.",
        "docs": "/docs",
        "health": "/health",
    }
