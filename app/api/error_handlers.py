from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import WeatherVibesError


async def handle_weather_vibes_error(_request: Request, exc: WeatherVibesError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(WeatherVibesError, handle_weather_vibes_error)
