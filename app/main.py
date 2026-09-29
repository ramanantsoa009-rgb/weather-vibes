"""Point d'entrée de Weather Vibes : assemble la configuration, les services et les routes.

Lancement : uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

import httpx
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.error_handlers import register_error_handlers
from app.api.routes import health, pages, weather
from app.config import Settings
from app.services import OpenWeatherClient, VibeMapper, WeatherService

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = Settings()
    timeout = httpx.Timeout(settings.REQUEST_TIMEOUT_SECONDS, connect=settings.CONNECT_TIMEOUT_SECONDS)

    # Un client HTTP par process (pool de connexions) : aucun état métier conservé.
    async with httpx.AsyncClient(timeout=timeout) as http_client:
        app.state.weather_service = WeatherService(
            client=OpenWeatherClient(http_client, settings),
            vibe_mapper=VibeMapper(),
        )
        yield


def create_app() -> FastAPI:
    app = FastAPI(title="Weather Vibes", version="1.0.0", lifespan=lifespan)
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    app.include_router(pages.router)
    app.include_router(health.router)
    app.include_router(weather.router)
    register_error_handlers(app)
    return app


app = create_app()
